from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from database.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    
    __tablename__ = "users"

    id= Column(Integer, primary_key=True)
    username = Column(String(50), unique=True,)
    first_name = Column(String(50))
    last_name= Column(String(50), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(Text)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    blogs = relationship("Blogs", back_populates="user")
    
    @property
    def serializer(self):
        dic = {}

        dic["id"] = self.id
        dic["first_name"] = self.first_name
        dic["last_name"] = self.last_name
        dic["email"] = self.email
        dic["is_active"]= self.is_active

        return dic
    
    
    