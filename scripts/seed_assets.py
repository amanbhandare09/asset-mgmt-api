import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import create_app
from app.extensions import db
from app.models.cashback_asset import CashbackAsset
from datetime import datetime, timedelta


app = create_app()

with app.app_context():

    assets = [
        CashbackAsset(
            title="Signup Bonus",
            total_value=100,
            expires_at=datetime.utcnow() + timedelta(days=30)
        ),
        CashbackAsset(
            title="Referral Reward",
            total_value=200,
            expires_at=datetime.utcnow() + timedelta(days=15)
        ),
        CashbackAsset(
            title="Festive Cashback",
            total_value=150
        )
    ]

    db.session.add_all(assets)
    db.session.commit()

    print("Seed data inserted ✅")
