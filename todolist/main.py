import uvicorn
import logging
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from api.webhooks import webhooks_router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


app = FastAPI(
    webhooks=webhooks_router,
)

app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
