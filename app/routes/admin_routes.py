from flask import Blueprint, request, render_template
from app.extensions import db
from app.models.cashback_asset import CashbackAsset
from app.models.claim_ledger import CashbackClaimLedger
from app.models.user import User
from app.middleware.session_guard import login_required
from app.middleware.rbac import admin_required
from datetime import datetime
from flask import redirect, url_for



admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@admin_required
def admin_dashboard():

    assets = CashbackAsset.query.all()

    return render_template(
        "admin/dashboard.html",
        assets=assets
    )

@admin_bp.route("/assets/create", methods=["POST"])
@login_required
@admin_required
def create_asset():

    data = request.get_json()

    if not data:
        return {"error": "No data"}, 400

    asset = CashbackAsset(
        title=data["title"],
        total_value=data["value"],
        status="AVAILABLE"
    )

    db.session.add(asset)
    db.session.commit()

    return {"message": "Asset created successfully"}

@admin_bp.route("/assets/<int:asset_id>/update", methods=["PATCH"])
@login_required
@admin_required
def update_asset(asset_id):

    asset = CashbackAsset.query.get(asset_id)

    if not asset:
        return {"error": "Asset not found"}, 404

    if asset.status == "CLAIMED":
        return {
            "error": "Cannot edit claimed asset"
        }, 400

    data = request.get_json()

    asset.title = data.get("title", asset.title)
    asset.total_value = data.get(
        "value",
        asset.total_value
    )

    db.session.commit()

    return {"message": "Updated successfully"}

@admin_bp.route("/assets/<int:asset_id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_asset(asset_id):

    asset = CashbackAsset.query.get(asset_id)

    if not asset:
        return {"error": "Asset not found"}, 404

    if asset.status == "CLAIMED":
        return {
            "error": "Cannot delete claimed asset"
        }, 400

    db.session.delete(asset)
    db.session.commit()

    return {"message": "Deleted successfully"}

@admin_bp.route("/assets/<int:asset_id>/expire", methods=["PATCH"])
@login_required
@admin_required
def expire_asset(asset_id):

    asset = CashbackAsset.query.get(asset_id)

    if not asset:
        return {"error": "Asset not found"}, 404

    if asset.status == "CLAIMED":
        return {"error": "Already claimed"}, 400

    asset.status = "EXPIRED"
    db.session.commit()

    return {"message": "Expired successfully"}

@admin_bp.route("/assets/<int:asset_id>/recreate", methods=["POST"])
@login_required
@admin_required
def recreate_asset(asset_id):

    old_asset = CashbackAsset.query.get(asset_id)

    if not old_asset:
        return {"error": "Asset not found"}, 404

    if old_asset.status != "EXPIRED":
        return {
            "error": "Only expired assets can be recreated"
        }, 400

    data = request.get_json()

    new_asset = CashbackAsset(
        title=data.get("title", old_asset.title),
        total_value=data.get(
            "value",
            old_asset.total_value
        ),
        status="AVAILABLE"
    )

    db.session.add(new_asset)
    db.session.commit()

    return {"message": "Asset recreated successfully"}

@admin_bp.route("/vouchers")
@login_required
@admin_required
def vouchers():

    data = (
        db.session.query(
            CashbackAsset,
            User
        )
        .outerjoin(
            User,
            CashbackAsset.claimed_by == User.id
        )
        .all()
    )

    result = []

    for asset, user in data:
        result.append({
            "id": asset.id,
            "title": asset.title,
            "value": float(asset.total_value),
            "status": asset.status,
            "claimed_by": user.email if user else "—"
        })

    return render_template(
        "admin/vouchers.html",
        vouchers=result
    )

@admin_bp.route("/assets/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_asset():

    if request.method == "POST":

        title = request.form["title"]
        value = request.form["value"]
        expires_at = request.form.get("expires_at")

        expiry_dt = (
            datetime.fromisoformat(expires_at)
            if expires_at else None
        )

        asset = CashbackAsset(
            title=title,
            total_value=value,
            expires_at=expiry_dt,
            status="AVAILABLE"
        )

        db.session.add(asset)
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))

    return render_template(
        "admin/asset_form.html",
        asset=None
    )

@admin_bp.route(
    "/assets/<int:asset_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_asset_page(asset_id):

    asset = CashbackAsset.query.get_or_404(asset_id)

    if asset.status == "CLAIMED":
        return "Cannot edit claimed asset", 400

    if request.method == "POST":

        asset.title = request.form["title"]
        asset.total_value = request.form["value"]

        expires_at = request.form.get("expires_at")

        asset.expires_at = (
            datetime.fromisoformat(expires_at)
            if expires_at else None
        )

        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))

    return render_template(
        "admin/asset_form.html",
        asset=asset
    )


