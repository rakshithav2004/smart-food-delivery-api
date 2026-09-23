from celery import Celery
from celery.schedules import crontab


celery_app = Celery(
    "food_delivery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "check-pending-orders-every-5-minutes": {
        "task": "app.tasks.notification_tasks.check_pending_orders",
        "schedule": 300.0,
    },
}