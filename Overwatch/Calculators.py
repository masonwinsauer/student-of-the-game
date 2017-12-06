import numpy as np

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
