from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.blogs.schemas import *
from app.blogs.services import BlogModelCRUDServices
from database.session import get_db
from app.utils.jwt_auth import CustomAuth
from app.utils.response_model import api_response

router = APIRouter()

@router.get("/")
def hello():
    return {"message":"Hello Blogs"}

@router.post("/create-blog/")
def create_blog(schema: BlogCreateSchema, db:Session = Depends(get_db), auth_detail: dict = Depends(CustomAuth())):
    blog_service = BlogModelCRUDServices(db=db)
    user_id = auth_detail["user_id"]
    return blog_service.create_blog(schema=schema, user_id=user_id)

@router.post("/update-blog/")
def update_blog(schema: BlogUpdateSchema, db:Session = Depends(get_db), auth_detail: dict = Depends(CustomAuth())):
    blog_service = BlogModelCRUDServices(db=db)
    user_id = auth_detail["user_id"]
    return blog_service.update_blog(schema=schema, user_id=user_id)

@router.get("/get_all_blogs/")
def get_all_blogs(offset, limit, db:Session = Depends(get_db), auth_detail: dict = Depends(CustomAuth())):
    blog_service = BlogModelCRUDServices(db=db)
    return blog_service.get_all_blogs(offset=offset, limit=limit)

@router.get("/get_blog_user/")
def get_blog_user(offset, limit, user_id: int = None, db:Session = Depends(get_db), auth_detail: dict = Depends(CustomAuth())):
    if not user_id:
        user_id= auth_detail["user_id"]

    blog_service = BlogModelCRUDServices(db=db)
    return blog_service.get_user_blog(offset=offset, limit=limit, user_id=user_id)



