from urllib.request import Request, urlopen
import urllib.parse
import json
import csv

complist = []

class APITools:
    def loadUsersFromCsv(filename):
        with open(filename, "rt") as f:
            return list(f)

    def getDataForUser(jsonurl):
        req = Request(jsonurl, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as url:
            player_data = json.loads(url.read().decode())
            comprank = player_data['us']['stats']['competitive']['overall_stats']['comprank']
            if comprank is not None:
                complist.append(comprank)

if __name__ == "__main__":
    for u in APITools.loadUsersFromCsv("users.csv"):
        jsonurl = urllib.parse.quote("http://localhost:4444/api/v3/u/" + str(u) + "/blob", safe=':/')
        print(jsonurl)
        try:
            APITools.getDataForUser(jsonurl)
        except (urllib.error.URLError, urllib.error.HTTPError):
            print("Retrieval of record for user at " + jsonurl + " failed.")
    print("AVERAGE SR: " + str(sum(complist) / float(len(complist))) + " !")
