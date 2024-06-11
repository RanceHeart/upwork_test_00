from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database
from ..dependencies import auth

router = APIRouter()


@router.post('/addpost', response_model=schemas.post.Post)
def add_post(post: schemas.PostCreate, token: str = Depends(auth.oauth2_scheme),
             db: Session = Depends(database.get_db)):
    try:
        user = auth.get_current_user(token=token, db=db)
        return crud.create_post(db=db, post=post, user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/getposts', response_model=List[schemas.post.Post])
def get_posts(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        user = auth.get_current_user(token=token, db=db)
        return crud.get_posts_by_user(db=db, user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/deletepost/{post_id}')
def delete_post(post_id: int, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        user = auth.get_current_user(token=token, db=db)
        post = crud.post.get_post(db=db, post_id=post_id)
        if not post or post.owner_id != user.id:
            raise HTTPException(status_code=400, detail="Post not found or not authorized")
        return crud.delete_post(db=db, post_id=post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
