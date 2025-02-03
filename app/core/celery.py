from celery import Celery
from app.core.config import settings


celery = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_expires=3600,
)
