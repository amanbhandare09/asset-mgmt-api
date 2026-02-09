from flask import Blueprint, request, render_template, session
from app.extensions import db
from app.models.cashback_asset import CashbackAsset
from app.models.claim_ledger import CashbackClaimLedger
from app.models.user import User
from app.middleware.session_guard import login_required
from app.middleware.rbac import admin_required


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@admin_required
def admin_dashboard():

    return render_template(
        "admin/dashboard.html",
        role=session.get("role")
    )

@admin_bp.route("/create-asset")
@login_required
@admin_required
def create_asset_page():

    return render_template(
        "admin/create_asset.html",
        role=session.get("role")
    )

@admin_bp.route("/assets/create", methods=["POST"])
@login_required
@admin_required
def create_asset():

    data = request.get_json()

    title = data.get("title")
    value = data.get("value")

    if not title or not value:
        return {"error": "Missing title or value"}, 400

    asset = CashbackAsset(
        title=title,
        total_value=value
    )

    db.session.add(asset)
    db.session.commit()

    return {"message": "Asset created successfully"}

@admin_bp.route("/assets/<int:asset_id>/expire", methods=["PATCH"])
@login_required
@admin_required
def expire_asset(asset_id):

    asset = CashbackAsset.query.get(asset_id)

    if not asset:
        return {"error": "Asset not found"}, 404

    if asset.status == "CLAIMED":
        return {
            "error": "Cannot expire a claimed asset"
        }, 400

    asset.status = "EXPIRED"
    db.session.commit()

    return {"message": "Asset expired successfully"}

@admin_bp.route("/ledger", methods=["GET"])
@login_required
@admin_required
def view_ledger():

    claims = (
        db.session.query(
            CashbackClaimLedger,
            CashbackAsset,
            User
        )
        .join(
            CashbackAsset,
            CashbackClaimLedger.asset_id == CashbackAsset.id
        )
        .join(
            User,
            CashbackClaimLedger.user_id == User.id
        )
        .all()
    )

    result = []

    for ledger, asset, user in claims:
        result.append({
            "asset": asset.title,
            "claimed_by": user.email,
            "amount": float(ledger.amount),
            "claimed_at": ledger.claimed_at
        })

    return {"ledger": result}


@admin_bp.route("/ledger-page")
@login_required
@admin_required
def ledger_page():

    claims = (
        db.session.query(
            CashbackClaimLedger,
            CashbackAsset,
            User
        )
        .join(CashbackAsset)
        .join(User)
        .all()
    )

    ledger_data = []

    for ledger, asset, user in claims:
        ledger_data.append({
            "asset": asset.title,
            "claimed_by": user.email,
            "amount": float(ledger.amount),
            "claimed_at": ledger.claimed_at
        })

    return render_template(
        "admin/ledger.html",
        ledger=ledger_data,
        role=session.get("role")
    )


@admin_bp.route("/analytics", methods=["GET"])
@login_required
@admin_required
def pool_analytics():

    total_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).scalar() or 0

    claimed_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).filter(
        CashbackAsset.status == "CLAIMED"
    ).scalar() or 0

    expired_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).filter(
        CashbackAsset.status == "EXPIRED"
    ).scalar() or 0

    return {
        "total_value": float(total_value),
        "claimed_value": float(claimed_value),
        "expired_value": float(expired_value),
        "remaining_liability": float(total_value - claimed_value)
    }

@admin_bp.route("/analytics-page")
@login_required
@admin_required
def analytics_page():

    total_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).scalar() or 0

    claimed_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).filter(
        CashbackAsset.status == "CLAIMED"
    ).scalar() or 0

    expired_value = db.session.query(
        db.func.sum(CashbackAsset.total_value)
    ).filter(
        CashbackAsset.status == "EXPIRED"
    ).scalar() or 0

    stats = {
        "total_value": float(total_value),
        "claimed_value": float(claimed_value),
        "expired_value": float(expired_value),
        "remaining_liability": float(total_value - claimed_value)
    }

    return render_template(
        "admin/analytics.html",
        stats=stats,
        role=session.get("role")
    )
