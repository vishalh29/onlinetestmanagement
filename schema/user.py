from pydantic import BaseModel
from typing import Optional
from enums import UserRole

class UserBase(BaseModel):
    username:str
    

class UserCreate(UserBase):
    password:str
    role:Optional[UserRole]="user"

        
class TestAttempt(BaseModel):
    answer:Optional[str]=None

class ViewTestAttempt(TestAttempt):
    test_id :int
    score :Optional[int]

class UserQuizBase(BaseModel):
    id:int
    test_id:int
    question_text:str
    correct_ans:str