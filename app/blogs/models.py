from database.base import Base
from sqlalchemy import Text, String, Column, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Blogs(Base):

    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="blogs")

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

        return dic