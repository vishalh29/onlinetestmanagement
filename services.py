
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User as UserModal
from fastapi import HTTPException,Depends
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime,timezone,timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashed password

def get_password_hash(password):
    return pwd_context.hash(password)

# verify hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# check user (Username)
def check_user(user,db:Session):
    obj=db.query(UserModal).filter(UserModal.username==user.username).first()
    if not obj :
        return None
    return obj

# get current user 
def get_current_user(db:Session,token: str = Depends(oauth2_scheme)):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_id:int= payload.get("user_id")
    if user_id is None:
        return None
    user=db.query(UserModal).filter(UserModal.id == user_id).first()
    return user



# create new user 
def create_new_user(user,db:Session):
    user_obj=check_user(user,db)
    if not user_obj:
        hashed_password=get_password_hash(user.password)
        userdata=UserModal(username=user.username,hashed_password=hashed_password,role=user.role)
        db.add(userdata)
        db.commit()
        return True
    return False

# create token
def create_token(user_id:int,username:str):
    payload={"user_id":user_id,"username":username}
    timee=datetime.now(timezone.utc)+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp":timee})
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


# verify token is valid (Expire or not) 
def check_token_validity(token: str = Depends(oauth2_scheme)):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    exp:int= payload.get("exp")
    if datetime.fromtimestamp(exp,tz=timezone.utc)  > datetime.now(timezone.utc):
        return True
    return False 

# authenticate user
def authenticate_user(userdata,db:Session):
    user = check_user(userdata,db)
    if not user:
        return False
    if not verify_password(userdata.password, user.hashed_password):
        return False
    return user





