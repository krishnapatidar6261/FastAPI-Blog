from pydantic import BaseModel


class BlogCreateSchema(BaseModel):
    title: str
    content: str

class BlogIDSchema(BaseModel):
    id: int

class BlogUpdateSchema(BlogIDSchema):
    title: str
    content: str

class BlogPagination(BaseModel):
    offset: int
    limit: int

class UserBlogSchema(BlogPagination):
    user_id: int

    
    