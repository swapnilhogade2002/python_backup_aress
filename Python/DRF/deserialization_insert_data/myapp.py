import requests
import json

URL="http://127.0.0.1:8585/createstu/"

data={
  'name':'geeks',
  'roll':108,
  'city':'Nashik'
}

json_data=json.dumps(data)

r=requests.post(url=URL, data=json_data)
data=r.json()
print(data)