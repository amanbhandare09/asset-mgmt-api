from flask import Blueprint, render_template, session
from app.models.cashback_asset import CashbackAsset
from app.middleware.session_guard import login_required

cashback_bp = Blueprint("cashback", __name__)

@cashback_bp.route("/dashboard")
@login_required
def dashboard_page():

    assets = CashbackAsset.query.all()

    return render_template(
        "user/dashboard.html",
        assets=assets,
        role=session.get("role")
    )

from app.models.claim_ledger import CashbackClaimLedger
from app.extensions import db

@cashback_bp.route("/claims")
@login_required
def claims_page():

    user_id = session.get("user_id")

    claims = (
        db.session.query(
            CashbackClaimLedger,
            CashbackAsset
        )
        .join(CashbackAsset)
        .filter(CashbackClaimLedger.user_id == user_id)
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

