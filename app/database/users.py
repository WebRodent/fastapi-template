import logging

from sqlalchemy.orm import Session

from app.models import User  # Assuming you have a UserModel in app.models
from app.schemas import UserRegister

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserRegister) -> User:
    """Create a new user in the database."""
    logger.debug(f"Creating user {user.name} in the database")
    db_user = User(**user.model_dump())  # Convert pydantic model to ORM model
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User:
    """Retrieve a user from the database by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, limit: int) -> User:
    """Retrieve all users from the database."""
    return db.query(User).limit(limit).all()
