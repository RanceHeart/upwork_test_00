from sqlalchemy.orm import Session
from .. import models, schemas


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    try:
        db_post = models.Post(**post.model_dump(), owner_id=user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        raise e


def get_posts_by_user(db: Session, user_id: int):
    try:
        return db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    except Exception as e:
        raise e


def get_post(db: Session, post_id: int):
    try:
        return db.query(models.Post).filter(models.Post.id == post_id).first()
    except Exception as e:
        raise e


def delete_post(db: Session, post_id: int):
    try:
        db_post = get_post(db, post_id)
        if db_post:
            db.delete(db_post)
            db.commit()
        return db_post
    except Exception as e:
        db.rollback()
        raise e
