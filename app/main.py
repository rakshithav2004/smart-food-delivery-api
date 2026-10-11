
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config.database import client
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.restaurant_router import router as restaurant_router
from app.routers.menu_router import router as menu_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.delivery_router import router as delivery_router
from app.routers.payment_router import router as payment_router
from app.routers.notification_router import router as notification_router


# Configure application logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(title="Smart Food Delivery API")


# Global handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unexpected error on %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


# Register API routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(delivery_router)
app.include_router(payment_router)
app.include_router(notification_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        await client.admin.command("ping")

        return {
            "status": "UP",
            "database": "MongoDB connected"
        }

    except Exception as e:
        logger.exception("Health check failed")

        return {
            "status": "DOWN",
            "database": "MongoDB connection failed",
            "error": str(e)
        }
