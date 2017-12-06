from urllib.request import Request, urlopen
from datetime import datetime
import urllib.parse
import json
import numpy as np
import sys
import csv

#TODO: Make Non-Global
complist = []

#TODO: Switch to argparse
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
            
        #ELO according to Blizzard
        if player_data['us']['stats']['competitive'] is not None:
            comprank = player_data['us']['stats']['competitive']['overall_stats']['comprank']
            if comprank is not None:
                #Add it to the global list if they placed
                complist.append(comprank)
        
            #This array only consists of heroes they have non-zero amounts of time on in competitive play
            hero_list = list(player_data['us']['heroes']['stats']['competitive'].keys())
            if len(hero_list) > 0 :
            
                #This is the distribution table of time spent on each hero they have played this season 
                dist = [[0 for x in range(len(hero_list))] for y in range(2)]
                
                #To normalize time on each hero against, we need all of the time they have played this season in Hours
                comptime = 0.0
                
                #Populate
                #TODO: Optimize
                for hero in hero_list:
                    hero_time = player_data['us']['heroes']['playtime']['competitive'][hero]
                    comptime += hero_time
                    idx = hero_list.index(hero) 
                    dist[0][idx] = hero

                ##Normalization of time on each hero   
                for hero in hero_list:
                    hero_time = player_data['us']['heroes']['playtime']['competitive'][hero]
                    idx = hero_list.index(hero) 
                    dist[1][idx] = hero_time / comptime

                dev = Calculators.getHeroStd(list(dist[1]))
                #print("Standard Dev for heroes: " + str(dev))

class Calculators:
    #Calculates the average of all SRs from the list
    def getAvgSr(cl):
        s = sum(cl)
        l = len(cl)
        if s > 0 and l > 0 :
            return round(s / float(l), 2)
   
    #Get standard deviation based on hero list. We will later want to correlate it with amount of time represented
        #Basically, if you have flatness across heroes, but not enough play time, it really doesn't mean much, and could in fact mean that you're being bullied into roles you don't normally play. Thus the performance-based SR gains/losses can be used to validate if someone who is flexible is good flexible or bad flexible.
    def getHeroStd(dist):
        return np.std(np.asarray(dist, dtype=float))
        

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
        #print(jsonurl)
        try:
            APITools.getDataForUser(jsonurl)
        except (urllib.error.URLError, urllib.error.HTTPError):
            print("Retrieval of record for user at " + jsonurl + " failed.")
    print("AVERAGE SR: " + str(Calculators.getAvgSr(complist)) + " calculated at: " + str(datetime.now()))
    
    DBTools.writeRecordToFile(str(datetime.now()) + " " + str(Calculators.getAvgSr(complist)) + "\n")
