from urllib.request import Request, urlopen
import json
import csv

with open("users.csv", "rt") as f:
    user_list = list(csv.reader(open("users.csv", "rt")))
    for u in user_list:
        print(u)

user = "Orange-12457"
jsonurl = "https://owapi.net/api/v3/u/" + user + "/blob"

#def getDataForUser():
req = Request(jsonurl, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req) as url:
    player_data = json.loads(url.read().decode())
    #print(player_data)
