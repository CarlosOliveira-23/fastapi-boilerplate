import aioredis
from fastapi import FastAPI
from app.core.config import settings

redis = None  # Variável global para o cliente Redis

async def init_redis():
    """Inicia a conexão com o Redis."""
    global redis
    redis = await aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses="True")

async def close_redis():
    """Fecha a conexão com o Redis ao desligar o app."""
    global redis
    if redis:
        await redis.close()
