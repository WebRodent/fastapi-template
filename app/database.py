from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import User
import os

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_user(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db, user: UserRegister):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
