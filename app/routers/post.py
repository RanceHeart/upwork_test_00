from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from .. import crud, schemas, database
from ..dependencies import auth
from cachetools import TTLCache
from fastapi.responses import JSONResponse
import json

router = APIRouter()

cache = TTLCache(maxsize=100, ttl=300)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post('/addpost', response_model=schemas.Post, summary="Add Post", description="Create a new post for the authenticated user.")
def add_post(post: schemas.PostCreate, token: str = Security(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Create a new post for the authenticated user. Validates the payload size to be under 1 MB.
    """
    try:
        user = auth.get_current_user(token=token, db=db)
        if len(post.text.encode('utf-8')) > 1024 * 1024:
            raise HTTPException(status_code=400, detail="Payload size exceeds 1 MB")
        return crud.create_post(db=db, post=post, user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/getposts', response_model=list[schemas.Post], summary="Get Posts", description="Retrieve all posts for the authenticated user with caching.")
def get_posts(token: str = Security(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Retrieve all posts for the authenticated user. Caches the response for up to 5 minutes.
    """
    try:
        user = auth.get_current_user(token=token, db=db)
        if user.id in cache:
            return JSONResponse(content=json.loads(cache[user.id]))
        posts = crud.get_posts_by_user(db=db, user_id=user.id)
        cache[user.id] = json.dumps(posts, default=str)
        return crud.get_posts_by_user(db=db, user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/deletepost/{post_id}', summary="Delete Post", description="Delete a post by ID for the authenticated user.")
def delete_post(post_id: int, token: str = Security(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Delete a post by its ID for the authenticated user.
    """
    try:
        user = auth.get_current_user(token=token, db=db)
        post = crud.post.get_post(db=db, post_id=post_id)
        if not post or post.owner_id != user.id:
            raise HTTPException(status_code=400, detail="Post not found or not authorized")
        return crud.delete_post(db=db, post_id=post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
