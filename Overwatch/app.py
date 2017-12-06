from urllib.request import Request, urlopen
from datetime import datetime
import urllib.parse
from Calculators import *
from APITools import *
from DBTools import *
import json
import sys
import csv

#TODO: Switch to argparse
userList = sys.argv[1]
outputFile = sys.argv[2]

complist = []

if __name__ == "__main__":
    for u in APITools.loadUsersFromCsv(userList):
        jsonurl = urllib.parse.quote("http://localhost:4444/api/v3/u/" + str(u) + "/blob", safe=':/')
        #print(jsonurl)
        try:
            #TODO: Define a new type for user data so we don't have to initialize an APITools object. That's just wrong.
            userdata = APITools()
            userdata.getDataForUser(jsonurl)
            #Add it to the global list if they placed
            complist.append(userdata.getCompRank())
        except (urllib.error.URLError, urllib.error.HTTPError):
            print("Retrieval of record for user at " + jsonurl + " failed.")
    print("AVERAGE SR: " + str(Calculators.getAvgSr(complist)) + " calculated at: " + str(datetime.now()))
    
    DBTools.writeRecordToFile(str(datetime.now()) + " " + str(Calculators.getAvgSr(complist)) + "\n", outputFile)
