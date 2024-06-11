from fastapi import FastAPI
from .routers import auth, post
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(post.router, prefix='/posts', tags=['posts'])
