from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import User, UserRole
from app.core.security import get_password_hash
from app.core.permissions import require_role, get_current_user
from app.core.redis import redis
from app.schemas.user import UserCreate, UserResponse
import json


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário com role (padrão: user)."""
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role or UserRole.USER  # 🔥 Define a role padrão como USER
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await redis.delete(f"user:{user_data.username}")

    return new_user


@router.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str, db: Session = Depends(get_db)):
    """Busca um usuário, primeiro no Redis, depois no banco."""

    cached_user = await redis.get(f"user:{username}")
    if cached_user:
        return json.loads(cached_user)  # Retorna cache

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await redis.setex(f"user:{username}", 300, json.dumps({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value
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


@router.get("/admin-only", dependencies=[Depends(require_role(UserRole.ADMIN))])
async def admin_only():
    """Apenas admins podem acessar essa rota."""
    return {"message": "Welcome, Admin!"}


@router.get("/manager-only", dependencies=[Depends(require_role(UserRole.MANAGER))])
async def manager_only():
    """Apenas managers podem acessar essa rota."""
    return {"message": "Welcome, Manager!"}


@router.get("/user-data", dependencies=[Depends(require_role(UserRole.USER))])
async def user_data():
    """Usuários normais podem acessar essa rota."""
    return {"message": "Welcome, User!"}
