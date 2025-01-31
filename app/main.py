from fastapi import FastAPI
from app.api.endpoints import auth, users
from app.core.sentry import init_sentry
from app.core.monitoring import init_monitoring
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

app = FastAPI()

init_sentry()

app.add_middleware(SentryAsgiMiddleware)

init_monitoring(app)

# Inclui rotas da API
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Boilerplate FastAPI funcionando!"}


@app.get("/error")
async def trigger_error():
    """Endpoint para testar o Sentry"""
    raise ValueError("Erro de teste para o Sentry!")
