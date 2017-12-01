from urllib.request import Request, urlopen
import urllib.parse
import json
import csv

def getDataForUser(jsonurl):
    req = Request(jsonurl, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as url:
        player_data = json.loads(url.read().decode())
        #print(player_data)

with open("users.csv", "rt") as f:
    user_list = list(csv.reader(open("users.csv", "rt")))
    for u in user_list:
        #user = "Orange-12457"
        jsonurl = urllib.parse.quote("http://localhost:4444/api/v3/u/" + str(u[0]) + "/blob", safe=':/')
        print(jsonurl)
        getDataForUser(jsonurl)
        #try:
        #except (urllib.error.URLError, urllib.error.HTTPError):
        #    print("Uh Ohhh")

