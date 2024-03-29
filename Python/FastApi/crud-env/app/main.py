from fastapi import FastAPI
from pydantic import BaseModel
from .import models
from database import engine

models.Base.metadata.create_all(engine)
app = FastAPI()

class Blog(BaseModel):
  title:str
  body:str
  
@app.post('/blog')
def create(request: schemas.blog,):
  return 'creating'