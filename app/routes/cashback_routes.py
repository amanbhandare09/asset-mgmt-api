from flask import Blueprint, render_template, session, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.cashback_asset import CashbackAsset
from app.models.claim_ledger import CashbackClaimLedger
from app.middleware.session_guard import login_required
from app.utils.redis_lock import RedisLock
from app.utils.limiter import limiter


cashback_bp = Blueprint("cashback", __name__)

@cashback_bp.route("/dashboard")
@login_required
def dashboard_page():

    assets = CashbackAsset.query.all()

    # Wallet balance aggregation
    balance = db.session.query(
        db.func.sum(CashbackClaimLedger.amount)
    ).filter(
        CashbackClaimLedger.user_id == session["user_id"]
    ).scalar() or 0

    return render_template(
        "user/dashboard.html",
        assets=assets,
        balance=float(balance),
        role=session.get("role")
    )

@cashback_bp.route("/<int:asset_id>/claim", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def claim_asset(asset_id):

    user_id = int(get_jwt_identity())

    lock = RedisLock(f"asset:{asset_id}")

    if not lock.acquire():
        return {"error": "Asset busy, retry"}, 429

    try:

        with db.session.begin():

            asset = (
                db.session.query(CashbackAsset)
                .filter_by(id=asset_id)
                .with_for_update()
                .first()
            )

            if not asset:
                return {"error": "Not found"}, 404

            if asset.status != "AVAILABLE":
                return {"error": "Already claimed"}, 400

            asset.status = "CLAIMED"
            asset.claimed_by = user_id

            ledger = CashbackClaimLedger(
                asset_id=asset.id,
                user_id=user_id,
                amount=asset.total_value
            )

            db.session.add(ledger)

        return {"message": "Claim successful"}

    finally:
        lock.release()


@cashback_bp.route("/claims")
@login_required
def claims_page():

    claims = (
        db.session.query(
            CashbackClaimLedger,
            CashbackAsset
        )
        .join(CashbackAsset)
        .filter(
            CashbackClaimLedger.user_id == session["user_id"]
        )
        .all()
    )

    result = []

    for ledger, asset in claims:
        result.append({
            "title": asset.title,
            "amount": float(ledger.amount),
            "claimed_at": ledger.claimed_at
        })

    return render_template(
        "user/claims.html",
        claims=result,
        role=session.get("role")
    )

