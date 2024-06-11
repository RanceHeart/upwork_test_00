from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, database, utils
from ..dependencies import auth
from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.post('/signup', response_model=schemas.user.User)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/login')
def login(user: schemas.user.UserCreate, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        if not utils.token.verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        access_token = utils.token.create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
