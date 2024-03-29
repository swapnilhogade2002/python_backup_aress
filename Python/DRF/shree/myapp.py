import requests
import json

URL = "http://127.0.0.1:8000/studentinfo/"  # Corrected the variable name to match case
r = requests.get(url=URL)

# Check if the request was successful (status code 200)
if r.status_code == 200:
    data = r.json()
    print(data)
else:
    print("Failed to fetch data. Status code:", r.status_code)

