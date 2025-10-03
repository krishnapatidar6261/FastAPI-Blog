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

    def __repr__(self):
        return f"<Blog(id={self.id}, title='{self.title}')>"

    @property
    def serializer(self):
        dic = {}
        dic["id"] = self.id
        dic["title"] = self.title
        dic["content"] = self.content
        dic["created"] = self.created.isoformat()
        dic["updated"] = self.updated.isoformat()
        dic["author"] = self.user.serializer
        dic["hashtags"] = [hashtag.serializer for hashtag in self.hashtags]

        return dic