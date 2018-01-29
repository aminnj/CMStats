import requests
import json
from dateutil import parser

API_URL = "https://www.cubemania.org/api/puzzles/2/singles?user_id={}"
user_id = 1124

data = requests.get(API_URL.format(user_id)).json()

data = sorted(data, key=lambda x:parser.parse(x["created_at"]))
for row in data:
    print json.dumps(row)
