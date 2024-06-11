from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils.token import get_password_hash
from sqlalchemy.exc import SQLAlchemyError


def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(email=user.email, hashed_password=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError as e:
        raise e


def get_user(db: Session, user_id: int):
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except SQLAlchemyError as e:
        raise e
