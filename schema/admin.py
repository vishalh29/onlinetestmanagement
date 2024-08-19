from pydantic import BaseModel
from typing import Optional
from enums import UserRole

class AdminBase(BaseModel):
    username:str
    

class AdminCreate(AdminBase):
    password:str
    role:Optional[UserRole]="admin"


# test 
        
class TestBase(BaseModel):
    id:int
    title :str
    description :Optional[str]  

class TestCreate(BaseModel):
    title :str
    description :Optional[str]=None  

class TestUpdate(BaseModel):
    title :Optional[str]=None
    description :Optional[str] =None


# quiz 
class QuizBase(BaseModel):
    test_id:int
    question_text:str
    correct_ans:str



class CreateQuiz(QuizBase):
    pass

class UpdateQuiz(BaseModel):
    test_id:Optional[int]
    question_text:Optional[str]
    correct_ans:Optional[str]


# user test 
class UserResultBase(BaseModel):
    user_id:int
    quiz_id:int
    score:Optional[int]
    user_answer:Optional[str]

