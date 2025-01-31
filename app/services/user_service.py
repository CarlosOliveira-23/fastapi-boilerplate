from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserLogin
from app.core.security import get_password_hash


def create_user(db: Session, user_data: UserLogin):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        return None

    new_user = User(
        username=user_data.username,
        email=f"{user_data.username}@example.com",
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
