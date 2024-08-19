from sqlalchemy import Column, Integer, String, ForeignKey, Text,Boolean,Enum
from sqlalchemy.orm import relationship
from database import Base
from enums import UserRole


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(128))
    role=Column(Enum(UserRole))

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True)
    description = Column(Text, nullable=True)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    question_text = Column(Text)
    correct_ans=Column(Text)



class UserTest(Base):
    __tablename__ = 'user_tests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer, ForeignKey('questions.id'))
    user_answer=Column(Text)


