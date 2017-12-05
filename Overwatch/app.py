from urllib.request import Request, urlopen
from datetime import datetime
import urllib.parse
import json
import sys
import csv

complist = []
userList = sys.argv[1]
outputFile = sys.argv[2]

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

class Calculators:
    def getAvgSr(cl):
        s = sum(cl)
        l = len(cl)
        if s > 0 and l > 0 :
            return round(s / float(l), 2)
    
    #def predictFinalSr():
        #seasonDaysLeft = ?
        #SR trajectory/slope = ?
        #randomness = ?
            #Best if we can get as granular as possible, but we can't know when to poll to get the most out of the API
            #For the next game, we may want to write an eventing tool
        #flexibility = ?
            #distribution of time over number of heroes
        #performanceGainsFactor = ?
            #what we think it is based on SR gains/losses vs average over x|x>1 number of games
        #historyOfViolence = ?
            #what should we take into account here?
                #performace gains?
            #what should our window be?
                #in number of games or days?
        #randomForest
        #neuralNetworks
        #0-5000
        #Much of this is based on polling, obviously, but we can normalize vs num games played

class DBTools:
    def writeRecordToFile(record):
        with open(outputFile, "a") as f:
            f.write(record)

if __name__ == "__main__":
    for u in APITools.loadUsersFromCsv(userList):
        jsonurl = urllib.parse.quote("http://localhost:4444/api/v3/u/" + str(u) + "/blob", safe=':/')
        print(jsonurl)
        try:
            APITools.getDataForUser(jsonurl)
        except (urllib.error.URLError, urllib.error.HTTPError):
            print("Retrieval of record for user at " + jsonurl + " failed.")
    print("AVERAGE SR: " + str(Calculators.getAvgSr(complist)) + " calculated at: " + str(datetime.now()))
    
    DBTools.writeRecordToFile(str(datetime.now()) + " " + str(Calculators.getAvgSr(complist)) + "\n")
