
from fastapi import APIRouter,Depends,HTTPException
from schema.admin import AdminBase,AdminCreate,TestBase,TestCreate,TestUpdate,QuizBase,CreateQuiz,UpdateQuiz,UserResultBase
from database import get_db
from sqlalchemy.orm import Session
from services import create_new_user,authenticate_user,create_token,check_token_validity,get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated,List
from models import Test,Question,UserTest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

admin_router=APIRouter(prefix="/admin")
admin_test_router=APIRouter(prefix="/admin/test")
admin_quiz_router=APIRouter(prefix="/admin/quiz")
admin_user_router=APIRouter(prefix="/admin/user-data")
@admin_router.post("")


async def create_user(user:AdminCreate,db:Session=Depends(get_db)):
    res=create_new_user(user,db)
    if res:
        return {"message":"Create Admin Account Successfulyy"}
    raise HTTPException(status_code=400,detail="User Is already Created With this Username")
    

#  login for admin
@admin_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(form_data,db)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)
    token=create_token(user.id,user.username)
    return {"token":token,"token_type":"Bearer"}


# get all test
@admin_test_router.get("",response_model=List[TestBase])
async def get_all_test(db:Session=Depends(get_db),skip: int = 0, limit: int = 100):
    all_records=db.query(Test).offset(skip).limit(limit).all()
    return all_records


# create test 
@admin_test_router.post("")
async def Create_Test(test:TestCreate ,token: str ,db:Session=Depends(get_db)):
    token_valid=check_token_validity(token)
    if token_valid:
        current_user=get_current_user(db,token)
    if current_user.role!="admin":
        raise HTTPException(status_code=400,detail="you dont have access to create test")
    data=Test(**test.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message":"Create Test Successfully"}


# delte Test

@admin_test_router.delete("/{test_id}")
async def delte_test(test_id:int,token:str,db:Session=Depends(get_db)):
    exits=db.query(Test).filter(Test.id == test_id).first()
    if exits:
        db.delete(exits)
        db.commit()
    raise HTTPException(status_code=400,detail="Invalid Test ID")    


# update test 
@admin_test_router.put("/{test_id}")
async def update_test(test_id:int,token:str,data:TestUpdate,db:Session=Depends(get_db)):
    old_data=db.query(Test).filter(Test.id == test_id).first()
    if old_data:
        old_data.title=data.title or old_data.title
        old_data.description=data.description or old_data.description
        db.commit()
        db.refresh(old_data)
        return {"message":"Update Content Successfully"}
    raise HTTPException(status_code=400,detail="Invalid Test ID")   



# QUIZ =====

# get all Quiz
@admin_quiz_router.get("",response_model=List[QuizBase])
async def get_all_quiz(db:Session=Depends(get_db),skip: int = 0, limit: int = 100):
    all_records=db.query(Question).offset(skip).limit(limit).all()
    return all_records


# create 
@admin_quiz_router.post("")
async def Create_quiz(quiz:CreateQuiz,token:str,db:Session=Depends(get_db)):
    data=Question(**quiz.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message":"Create Quiz Successfully"}


# delte 
@admin_quiz_router.delete("/{quiz_id}")
async def delte_quiz(quiz_id:int,token:str,db:Session=Depends(get_db)):
    exits=db.query(Question).filter(Question.id == quiz_id).first()
    if exits:
        db.delete(exits)
        db.commit()
    raise HTTPException(status_code=400,detail="Invalid Quiz ID")    


# update 
@admin_quiz_router.put("/{quiz_id}")
async def update_quiz(quiz_id:int,token:str,data:UpdateQuiz,db:Session=Depends(get_db)):
    old_data=db.query(Question).filter(Question.id == quiz_id).first()
    if old_data:
        old_data.test_id=data.test_id or old_data.test_id
        old_data.question_text=data.question_text or old_data.question_text
        old_data.correct_ans=data.correct_ans or old_data.correct_ans
        db.commit()
        db.refresh(old_data)
        return {"message":"Update Quiz Content Successfully"}
    raise HTTPException(status_code=400,detail="Invalid Quiz ID")   

@admin_user_router.get("",response_model=List[UserResultBase])
def show_all_user_result(db:Session=Depends(get_db),skip: int = 0, limit: int = 100):
    all_records=db.query(UserTest).offset(skip).limit(limit).all()
    return all_records
