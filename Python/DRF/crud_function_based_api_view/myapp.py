import requests
import json

URL = "http://127.0.0.1:8000/studentapi/"

# Getting data
def get_data(id=None):
    params = {}
    if id is not None:
        params = {'id': id}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.get(url=URL, params=params, headers=headers)
        r.raise_for_status()  # Raise an exception for any error status code
        
        data = r.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# get_data(1)

# Posting data
def post_data():
    data = {
        'name': 'swapnil',
        'roll': 151,
        'city': 'Hyderabad'
    }
  
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url=URL, data=json_data, headers=headers)
        r.raise_for_status()
        
        print("Data inserted successfully")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# post_data()

# Updating data
def update_data():
    data = {
        'id': 2,
        'name': 'jyoti',
        'roll': 122,
        'city': 'Bangalore'
    }
  
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'} 
    
    try:
        r = requests.put(url=URL, data=json_data, headers=headers)
        r.raise_for_status()  
        
        print("Data updated successfully")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# update_data()

# Deleting data
def delete_data():
  data={'id':2}
  json_data=json.dumps(data)
  headers = {'content-Type': 'application/json'}
  r=requests.delete(url=URL,headers=headers, data=json_data)
  data=r.json()
  print(data)
  
# delete_data()