from pydantic import BaseModel, EmailStr, root_validator
from typing import Optional



class UserRegistrationSchema(BaseModel):

    username: str
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    password: str
    confirm_password: str


    @root_validator(skip_on_failure=True)
    def passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw != cpw:
            raise ValueError('Password and Confirm Password do not match')
        return values
    

class UserLoginSchema(BaseModel):

    username: str
    password: str