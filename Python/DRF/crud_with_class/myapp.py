import requests
import json

URL="http://127.0.0.1:8000/studentapi/"

#getting all data
def get_data(id=None):
  data={}
  if id is not None:
    data={'id':id}
  json_data=json.dumps(data)
  r=requests.get(url=URL, data=json_data)
  data=r.json()
  print(data)
  
# get_data()

#posting data
def post_data():
  data={
    'name':'khushbu',
    'roll':112,
    'city':'Hydrabad'
  }
  
  json_data=json.dumps(data)
  r=requests.post(url=URL, data = json_data)
  data=r.json()
  print(data)
  
# post_data() 

#updating data
def update_data():
  data={
    'id':4,
    'name':'jyoti',
    'roll':122,
    'city':'Banglore'
  }
  
  json_data=json.dumps(data)
  r=requests.put(url=URL,data=json_data)
  data=r.json()
  print(data)

# update_data()

def delete_data():
  data={'id':5}
  json_data=json.dumps(data)
  r=requests.delete(url=URL, data=json_data)
  data=r.json()
  print(data)
  
delete_data()
  
  
  
    