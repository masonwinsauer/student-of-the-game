from urllib.request import Request, urlopen
import urllib.parse

from datetime import datetime

import json
import sys
import csv

from Calculators import *
from APITools import *
from DBConn import *
from UserData import *

#TODO: Switch to argparse
userList = sys.argv[1]
outputFile = sys.argv[2]

complist = []

if __name__ == "__main__":
    conn = DBConn(outputFile)
    for u in APITools.loadUsersFromCsv(userList):
        jsonurl = urllib.parse.quote("http://localhost:4444/api/v3/u/" + str(u) + "/blob", safe=':/')
        print(u)
        try:
            # Attempt to get the JSON blob for a user
            blob = APITools.getDataForUser(jsonurl)
            
            # Create a UserData object to hold information about the active user
            uData = UserData()
            uData.processBlob(blob)

            # Add their competitive rank to the global list if they placed
            cr = uData.getCompRank()
            if cr is not None:
                complist.append(cr)
            
            # Get the hero distribution for the user
            dist = uData.getHeroDist()
            if dist is not None:
                # Calculate the standard deviation of the list
                std = Calculators.getHeroStd(dist[1])

                print("\tStandard Deviation for Heroes: " + str(std))
                
                conn.writeRecordToFile("User: " + u + "Hero STD: " + str(std) + "\n")
        
        except (urllib.error.URLError, urllib.error.HTTPError):
            print("Retrieval of record for user at " + jsonurl + " failed.")
    
    print("AVERAGE SR: " + str(Calculators.getAvgSr(complist)) + " calculated at: " + str(datetime.now()))
    conn.writeRecordToFile(str(datetime.now()) + " " + str(Calculators.getAvgSr(complist)) + "\n")
    conn.closeFile(outputFile)
