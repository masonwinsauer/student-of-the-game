from urllib.request import Request, urlopen
import json

user = "Orange-12457"
jsonurl = "https://owapi.net/api/v3/u/" + user + "/blob"

req = Request(jsonurl, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req) as url:
    player_data = json.loads(url.read().decode())
    print(player_data)
