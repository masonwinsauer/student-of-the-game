from urllib.request import Request, urlopen
import urllib.parse
import json

class APITools:

    def __init__(self):
        self.rank = -1
        self.heroDist = [[]]

    def loadUsersFromCsv(filename):
        with open(filename, "rt") as f:
            return list(f)

    def getDataForUser(jsonurl):
        req = Request(jsonurl, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as url:
            return json.loads(url.read().decode())
