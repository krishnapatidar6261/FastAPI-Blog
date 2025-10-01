from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.schemas import UserRegistrationSchema, UserLoginSchema
from app.core.services import UserRegistrationLoginService
from database.session import get_db
from app.utils.jwt_auth import CustomAuth
from app.utils.response_model import api_response

router = APIRouter()


@router.get("/")
def hello():
    return {"message":"Hello World"}

@router.post("/register/")
def register(schema: UserRegistrationSchema, db:Session = Depends(get_db)):
    return UserRegistrationLoginService.register_user(db=db, schema=schema)

@router.post("/login/")
def login(schema: UserLoginSchema, db:Session = Depends(get_db)):
    return UserRegistrationLoginService.login_user(db=db, schema=schema)

@router.get("/my_profile/")
def my_profile(auth: dict = Depends(CustomAuth())):
    return api_response(200, data=auth, message="Fetched Successfully")

