from sqlalchemy.orm import Session
from app.core.models import Users      
from app.utils.response_model import api_response
from app.utils.hash_password import PassswordUtils
from app.utils.jwt_auth import JWTUtils

class UserRegistrationLoginService:

    @classmethod
    def check_username_exists(cls, db: Session, username):
        existing_user_by_username = db.query(Users).filter(Users.username == username).first()
        return existing_user_by_username

    @classmethod
    def register_user(cls, db: Session, schema):
        existing_user = cls.check_username_exists(db=db, username=schema.username)
        if existing_user:
            return api_response(400, message="Username already exists")
        
        hashed_password = PassswordUtils.hash_password(schema.password)
        new_user = Users(
                        username=schema.username,
                        first_name=schema.first_name,
                        last_name=schema.last_name,
                        is_active=False,
                        email = schema.email,
                        password=hashed_password,
                        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
       
        except Exception as e:
            db.rollback()
            return api_response(500, message=f"Something Went Wrong: {str(e)}")

        return api_response(200, data=new_user.serializer, message="Register successfully")

    @classmethod
    def login_user(cls, db:Session, schema):
        user_obj = cls.check_username_exists(db=db, username=schema.username )

        if not user_obj:
            return api_response(400, message="Username not exists")
        
        password_verified = PassswordUtils.verify_password(plain_password=schema.password, hashed_password=user_obj.password)
        if password_verified:
            payload = {"username": user_obj.username,
                       "user_id": user_obj.id,
                       "email": user_obj.email
                       }
            tokens_dic = JWTUtils.get_tokens_with_refresh(data=payload)
            user_obj.is_active =True
            db.commit()
            db.refresh(user_obj)

            return api_response(200, message="Username and Password verified", data=tokens_dic)
        
        return api_response(400, message="Username and Password not verified")
    

        

# class ProfileService:

#     @classmethod
#     def my_profile(cls, db:Session, token):
        
#         pass