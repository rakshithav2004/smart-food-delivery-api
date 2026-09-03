from fastapi import FastAPI
from app.config.database import client
from app.routers.auth_router import router as auth_router

app = FastAPI(title="Smart Food Delivery API")
app.include_router(auth_router)

@app.get("/health")
async def health_check():
    try:
        await client.admin.command("ping")
        return {
            "status": "UP",
            "database": "MongoDB connected"
        }
    except Exception as e:
        return {
            "status": "DOWN",
            "database": "MongoDB connection failed",
            "error": str(e)
        }