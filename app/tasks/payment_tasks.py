from app.config.celery_config import celery_app


@celery_app.task
def process_payment_notification(
    payment_id: str,
    status: str
):
    print(
        f"Payment {payment_id} "
        f"status changed to {status}"
    )

    return {
        "payment_id": payment_id,
        "status": status,
        "notification_status": "processed"
    }