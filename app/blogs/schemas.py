from pydantic import BaseModel
from typing import List, Optional

class BlogCreateSchema(BaseModel):
    title: str
    content: str
    hashtag_ids: Optional[List[int]]= None

class BlogIDSchema(BaseModel):
    id: int

class BlogUpdateSchema(BlogIDSchema):
    title: str
    content: str
    hashtag_ids: Optional[List[int]]= None

class PaginationBlogAppSchema(BaseModel):
    offset: int
    limit: int

class UserBlogSchema(PaginationBlogAppSchema):
    user_id: int

    
    