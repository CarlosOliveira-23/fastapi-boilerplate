from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import get_password_hash


def init_db(db: Session):
    user = db.query(User).first()
    if not user:
        new_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
