from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api.endpoints import auth, users
from app.core.sentry import init_sentry
from app.core.monitoring import init_monitoring
from app.core.admin import admin_app, init_admin
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from app.api.endpoints import ws
from app.core.redis import init_redis, close_redis

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.add_middleware(SentryAsgiMiddleware)

init_sentry()
init_monitoring(app)

app.include_router(ws.router, prefix="/ws", tags=["websockets"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    await init_admin()
    await init_redis()  # 🔥 Inicia o Redis
    app.mount("/admin", admin_app)

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()  # 🔥 Fecha a conexão Redis

@app.get("/")
def root():
    return {"message": "Boilerplate FastAPI funcionando!"}

@app.get("/error")
async def trigger_error():
    raise ValueError("Erro de teste para o Sentry!")
