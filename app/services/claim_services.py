from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.cashback_asset import CashbackAsset
from app.models.claim_ledger import CashbackClaimLedger
from app.extensions_redis import redis_client
import time


def claim_cashback_asset(asset_id, user_id):

    lock_key = f"lock:asset:{asset_id}"

    # Try acquiring lock
    lock = redis_client.set(
        lock_key,
        user_id,
        nx=True,   # Only if not exists
        ex=10      # Auto-expire in 10 sec
    )

    if not lock:
        return {"error": "Another claim in progress"}, 423

    try:
        # --- DB TRANSACTION START ---

        asset = (
            db.session.query(CashbackAsset)
            .filter(CashbackAsset.id == asset_id)
            .with_for_update()
            .first()
        )

        if not asset:
            return {"error": "Asset not found"}, 404

        if asset.status != "AVAILABLE":
            return {"error": "Asset already claimed"}, 409

        asset.status = "CLAIMED"
        asset.claimed_by = user_id
        asset.claimed_at = datetime.utcnow()

        ledger = CashbackClaimLedger(
            asset_id=asset.id,
            user_id=user_id,
            amount=asset.total_value
        )

        db.session.add(ledger)
        db.session.commit()

        return {"message": "Claim successful"}, 200

    finally:
        redis_client.delete(lock_key)