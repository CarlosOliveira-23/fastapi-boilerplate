from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import User
from app.core.security import get_password_hash
from app.core.redis import redis
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
async def register_user(user_data: User, db: Session = Depends(get_db)):
    """Registra um novo usuário e remove do cache para evitar dados desatualizados."""
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.username + "@example.com",  # Simulação
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await redis.delete(f"user:{user_data.username}")

    return {"message": "User registered successfully"}

@router.get("/users/{username}")
async def get_user(username: str, db: Session = Depends(get_db)):
    """Busca um usuário, primeiro no Redis, depois no banco."""

    # 1️⃣ Tenta buscar do cache
    cached_user = await redis.get(f"user:{username}")
    if cached_user:
        return json.loads(cached_user)  # Retorna cache

    # 2️⃣ Se não está no cache, busca no banco de dados
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3️⃣ Armazena no cache com expiração de 5 minutos
    await redis.setex(f"user:{username}", 300, json.dumps({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }))

    return user

@router.put("/users/{username}")
async def update_user(username: str, db: Session = Depends(get_db)):
    """Atualiza um usuário e limpa o cache"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = f"updated_{username}@example.com"
    db.commit()
    db.refresh(user)

    await redis.delete(f"user:{username}")

    return {"message": "User updated successfully"}
