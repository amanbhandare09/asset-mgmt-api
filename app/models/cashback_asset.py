from datetime import datetime
from app.extensions import db


class CashbackAsset(db.Model):
    __tablename__ = "cashback_assets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    total_value = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="AVAILABLE",
        nullable=False,
        index=True
    )

    claimed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # Optimistic locking support
    version = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    # Relationship → ledger
    claims = db.relationship(
        "CashbackClaimLedger",
        backref="asset",
        lazy=True
    )
