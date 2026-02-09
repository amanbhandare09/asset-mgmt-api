from datetime import datetime
from app.extensions import db


class CashbackClaimLedger(db.Model):
    __tablename__ = "cashback_claims_ledger"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    asset_id = db.Column(
        db.Integer,
        db.ForeignKey("cashback_assets.id"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    claimed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
