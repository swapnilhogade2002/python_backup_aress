
# http://127.0.0.1:8000/docs: it's for swagger UI
# http://127.0.0.1:8000/redoc : API Docs

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get('/')
def index():
  return "hello"

@app.get('/')
def index():
  return "data:{'name':'swapnil'}"

@app.get('/about/{id}')
def index(id:int):
  return {'data':id}

class Blog(BaseModel):
  title:str
  body:str
  published:Optional[bool]
 
@app.post('/blog')
def create_blog(blog: Blog):
  return{ 'data':f'blog is created.{blog.title}' }
  