import requests
import pandas as pd
import json

url = 'https://jsonplaceholder.typicode.com/'

response = requests.get(url=url+'todos/1')
print(response.status_code)

data = json.dumps(response.json(), indent=2)
print(data)
