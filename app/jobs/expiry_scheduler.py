from datetime import datetime
from app.extensions import db
from app.models.cashback_asset import CashbackAsset


def expire_assets_job(app):

    with app.app_context():

        now = datetime.utcnow()

        assets = CashbackAsset.query.filter(
            CashbackAsset.status == "AVAILABLE",
            CashbackAsset.expires_at != None,
            CashbackAsset.expires_at < now
        ).all()

        for asset in assets:
            asset.status = "EXPIRED"

        db.session.commit()

        print(f"[Scheduler] Expired {len(assets)} assets")
