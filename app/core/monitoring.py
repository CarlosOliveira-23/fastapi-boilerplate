from prometheus_fastapi_instrumentator import Instrumentator


def init_monitoring(app):
    Instrumentator().instrument(app).expose(app)
