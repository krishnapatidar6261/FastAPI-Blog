from database.base import Base
from sqlalchemy import Text, String, Column, Boolean, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.models import Users

blog_hashtag = Table(
    "blog_hashtag",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id"), primary_key=True),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id"), primary_key=True),
)

class HashTags(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    blogs = relationship(
        "Blogs",
        secondary=blog_hashtag,
        back_populates="hashtags"
    )

    @property
    def serializer(self):
        dic ={}
        dic["id"] = self.id
        dic["name"]= self.name
        return dic

class Blogs(Base):

    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="blogs")
    hashtags = relationship("HashTags",
                            secondary=blog_hashtag,
                            back_populates="blogs"
                        )

    likes = relationship("BlogLike", back_populates="blog", lazy="dynamic")

    def __repr__(self):
        return f"<Blog(id={self.id}, title='{self.title}')>"
    
    def serializer(self, user_id=None):
        dic = {}
        dic["id"] = self.id
        dic["title"] = self.title
        dic["content"] = self.content
        dic["created"] = self.created.isoformat()
        dic["updated"] = self.updated.isoformat()
        dic["author"] = self.user.serializer
        dic["hashtags"] = [hashtag.serializer for hashtag in self.hashtags]
        
        dic["is_liked"]= False
        if user_id:
            dic["is_liked"] = self.likes.filter_by(liked_by_user_id=user_id).first() is not None

        return dic
    
class BlogLike(Base):
    __tablename__ = "blog_likes"
    
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    liked_by_user_id = Column(Integer, ForeignKey("users.id"))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    blog = relationship("Blogs", back_populates="likes")
    liked_by = relationship("Users", back_populates="likes_given")

    def __repr__(self):
        return f"<BlogLike(id={self.id}, blog_id='{self.blog_id}'), Liked by='{self.liked_by_id}')>"
    
    def serializer(self, user_id=None):
        dic = {}
        dic["id"] = self.id
        dic["blog_details"] = self.blog.serializer(user_id=user_id)
        dic["user_details"] = self.liked_by.serializer

        return dic