from app.config.celery_config import celery_app


@celery_app.task
def send_order_notification(order_id: str, message: str):
    print(
        f"Notification for order {order_id}: {message}"
    )

    return {
        "order_id": order_id,
        "message": message,
        "status": "notification_processed"
    }


@celery_app.task
def send_order_status_notification(
    order_id: str,
    status: str
):
    print(
        f"Order {order_id} status changed to {status}"
    )

    return {
        "order_id": order_id,
        "status": status,
        "notification_status": "processed"
    }


@celery_app.task
def check_pending_orders():
    print("Checking pending orders...")

    return {
        "status": "completed",
        "message": "Pending orders checked successfully"
    }