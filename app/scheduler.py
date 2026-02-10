from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.expiry_scheduler import expire_assets_job


scheduler = BackgroundScheduler()


def start_scheduler(app):

    scheduler.add_job(
        func=expire_assets_job,
        trigger="interval",
        minutes=1,
        args=[app]   # pass app context
    )

    scheduler.start()
