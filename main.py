from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import Base,engine
from routes.admin import admin_router,admin_quiz_router,admin_test_router,admin_user_router
from routes.user import user_router



app = FastAPI()

app.include_router(prefix="/v1",router=admin_router,tags=["Admin Signup and Login"])
app.include_router(prefix="/v1",router=admin_quiz_router,tags=["Admin QUIZ"])
app.include_router(prefix="/v1",router=admin_test_router,tags=["Admin TEST"])
app.include_router(prefix="/v1",router=admin_user_router,tags=["View User Result"])
app.include_router(prefix="/v1",router=user_router,tags=["User"])

Base.metadata.create_all(bind=engine)







