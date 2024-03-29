from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

# class Blog(Base):
#   __tablename__='blogs'
  
#   id= Column(Integer, primary_key=True,index=True)
#   title=Column(String)
#   body=Column(String)


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
