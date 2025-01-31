import sentry_sdk
from app.core.config import settings


def init_sentry():
    """Inicializa o Sentry para capturar erros no sistema."""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0,
        )
