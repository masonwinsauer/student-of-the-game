from APITools import *

class UserData:
    
    def __init__(self):
        self.rank = -1
        self.heroDist = [[]]

    def processBlob(self, player_data):
        #ELO according to Blizzard
        if player_data['us']['stats']['competitive'] is not None:
            comprank = player_data['us']['stats']['competitive']['overall_stats']['comprank']
            if comprank is not None:
                self.rank = comprank
        
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

                self.heroDist = dist

    def getCompRank(self):
        if self.rank != -1 :
            return self.rank

    def getHeroDist(self):
        if len(self.heroDist[0]) > 0 :
            return self.heroDist
