
from fastapi import APIRouter,Depends,HTTPException
from schema.user import UserCreate,UserBase,ViewTestAttempt,TestAttempt
from database import get_db
from sqlalchemy.orm import Session
from services import create_new_user,authenticate_user,create_token,check_token_validity,get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Question,UserTest
from schema.user import UserQuizBase
from typing import List
user_router=APIRouter(prefix="/user")


@user_router.post("")
async def create_user(user:UserCreate,db:Session=Depends(get_db)):
    res= create_new_user(user,db)
    if res:
        return {"message":"Create User Account Successfulyy"}
    raise HTTPException(status_code=400,detail="User Is already Created With this Username")
    
# user login

#  login for admin
@user_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(form_data,db)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)
    token=create_token(user.id,user.username)
    return {"token":token,"token_type":"Bearer"}


@user_router.get("/all-quiz",response_model=List[UserQuizBase])
async def get_all_quiz(db:Session=Depends(get_db),skip: int = 0, limit: int = 100):
    all_records=db.query(Question).offset(skip).limit(limit).all()
    return all_records

# attempt test
@user_router.post("/quiz-test/{quiz_id}")
async def quiz_submit(test:TestAttempt,quiz_id:int,token:str,db:Session=Depends(get_db)):
    token_valid=check_token_validity(token)
    if token_valid:
        current_user=get_current_user(db,token)
        new_record=UserTest(user_id=current_user.id,quiz_id=quiz_id,score=0,user_answer=test.answer)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {"message":"test attempted successfully"}
    raise HTTPException(status_code=400,detail="unauthorised login again")