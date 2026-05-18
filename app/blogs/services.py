from app.blogs.models import Blogs, HashTags
from sqlalchemy.orm import Session
from app.blogs.schemas import BlogCreateSchema, BlogUpdateSchema, BlogIDSchema
from app.utils.response_model import api_response
from app.utils.paginations import Pagination

class BlogModelCRUDServices:
    def __init__(self, db:Session):
        self.db = db

    def save(self):
        try: 
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e

    def add_hashtags_blog(self, blog_obj, hashtag_ids:list[int]):

        hashtag_service = BlogHashTagsService(db=self.db)
        hashtags_queryset= hashtag_service.get_hashtag_queryset_by_ids(ids_list=hashtag_ids)
        blog_obj.hashtags = hashtags_queryset

        return True


    def create_blog(self,schema:BlogCreateSchema, user_id:int):
        blog_obj = Blogs(title = schema.title,
                        content= schema.content,
                        user_id= user_id
                        )
        
        if schema.hashtag_ids:
            self.add_hashtags_blog(hashtag_ids=schema.hashtag_ids, 
                                   blog_obj=blog_obj
                                   )

        try:
            self.db.add(blog_obj)
            self.save()

        except Exception as e:
            return api_response(500, message=f"Internal Server Error: {str(e)}")
        
        return api_response(200, data=blog_obj.serializer, message="Blog Created Successfully")


    def update_blog(self,user_id, schema: BlogUpdateSchema):
        
        blog = self.db.query(Blogs).filter(Blogs.id==schema.id).first()
        if not blog:
            return api_response(404, message="Blog not found")
        if blog.user_id != user_id:
            return api_response(403, message="You are not the blog author")
        
        blog.title = schema.title
        blog.content = schema.content

        if schema.hashtag_ids:
            self.add_hashtags_blog(hashtag_ids=schema.hashtag_ids, 
                                   blog_obj=blog
                                   )
        try:
            self.save()
        except Exception as e:
            return api_response(500, message=f"Internal Server error: {str(e)}")

        return api_response(200, message="Blog Updated Successfully", data= blog.serializer)

    def get_all_blogs(self, offset, limit):
        queryset = self.db.query(Blogs).order_by(Blogs.created.desc())
        pagination_obj = Pagination(offset=offset,
                                    limit=limit 
                                    )
        paginated_res = pagination_obj.queryset_level_pagination(queryset=queryset)
        paginated_res["results"] = [obj.serializer for obj in paginated_res["results"]]

        return api_response(200, message="fetched successfully", data=paginated_res)

    def get_user_blog(self, user_id, offset, limit):
        queryset = self.db.query(Blogs).order_by(Blogs.created.desc()).filter(Blogs.user_id== user_id)
        pagination_obj = Pagination(offset=offset,
                                    limit=limit 
                                    )
        paginated_res = pagination_obj.queryset_level_pagination(queryset=queryset)
        paginated_res["results"] = [obj.serializer for obj in paginated_res["results"]]

        return api_response(200, message="fetched successfully", data=paginated_res)
    

    def delete_blog(self, user_id, schema: BlogIDSchema):
        blog = self.db.query(Blogs).filter(Blogs.id == schema.id).first()
        if not blog:
            return api_response(404, message="Blog Not exists")
        
        if blog.user_id != user_id:
            return api_response(403, message="You are not author of this blog")
        self.db.delete(blog)

        try:
            self.save()
        except Exception as e:
            return api_response(500, message=f"Internal Server error: {str(e)}")
        
        return api_response(200, message="Blog Deleted successfully")

class DBPingService:
    def __init__(self, db:Session):
        self.db = db

    def save(self):
        try: 
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
    
class BlogHashTagsService(DBPingService):
    def get_all_hashtags(self, offset, limit):
        queryset= self.db.query(HashTags).order_by(HashTags.id.desc())
        pagination_obj = Pagination(offset=offset, limit= limit)
        paginated_res = pagination_obj.queryset_level_pagination(queryset=queryset)
        paginated_res["results"] = [obj.serializer for obj in paginated_res["results"]]

        return api_response(status_code=200, message="Fetched Successfully", data=paginated_res)

    def get_hashtag_queryset_by_ids(self, ids_list):
        hashtag_queryset = self.db.query(HashTags).filter(HashTags.id.in_(ids_list)).all()
        return hashtag_queryset