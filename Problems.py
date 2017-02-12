#!/usr/bin/env python2
from random import random,sample,choice, shuffle
import solveAgent
import util
import os   # for detecting *nix
import math

""" Source: https://github.com/kushjain/Min-Conflicts
    This file includes problem definitons"""


##########################################################
# AreaCoverage
##########################################################
        
class AreaCoverage:
    """ In this, we attempt to place N UAVs and M boats in NxN area in such a way
    that the coverage area is maximized by minimizing the overlap """
    
    def __init__(self, N, UAVNumber, UAVRadius, boatNumber, boatRadius, numTestStates):
        self.size = N
        self.UAVnumber=UAVNumber
        self.UAVRadius=UAVRadius
        self.boatNumber=boatNumber
        self.boatRadius=boatRadius
        self.numTestStates=numTestStates
        self.valDomainUAV = [UAVRadius, N-UAVRadius]  #The Value domain from which variables can take value
        self.valDomainBoat=[boatRadius, N-boatRadius]
        self.board = [0, N]     #We are only making one dimensional array as opposed to matrix and enforcing different row constraint here itself
        self.ObjList=dict()
    
    #get the starter state
    def getStartState(self):
        """We have done random assignments, (somewhat greedily). However, a greedy assignments may be used to improve performance"""
        #Forcing Column Constraint randomly
        for i in range(self.UAVnumber):
            self.ObjList[str(i)+'u']=(random.uniform(self.valDomainUAV[0], self.valDomainUAV[1]), random.uniform(self.valDomainUAV[0], self.valDomainUAV[1]),self.UAVRadius,0)
        for j in range(self.boatNumber):
            self.ObjList[str(j)+'b']=(random.uniform(self.valDomainBoat[0], self.valDomainBoat[1]), random.uniform(self.valDomainBoat[0], self.valDomainBoat[1]), self.boatRadius,0)
        return self.ObjList


    def isConflicting(self, state, var):  #returns true if the var overlaps another objects, otheriwse returns false
        currObj=state[var]
        for k, v in state.items():
            if(k==var):
                continue
            if(self.getOverlapDistance(currObj, state[k])>0):
                return True
        return False
        
    # returns the value of radius1+radius2-distance between centers if it is positive
    def getOverlapDistance(self, var1, var2):
        overLapDistance = max(float(var1[2])+float(var2[2])-self.calculateDirectDistance(var1,var2), 0)
        return overLapDistance  
    
    # Uses the Pythagorean Theorem to find the direct distance between objects var1 and var2
    def calculateDirectDistance(self, var1, var2):
        return math.sqrt(float(float(var1[0]-var2[0])**2+float(var1[1]-var2[1])**2))
        
    # randomly picks any UAV/boat which is still overlapping. Returns -1 if none of the objects are overlapping 
    def getVar(self, state):     
        varPool = sample(self.ObjList.keys(), len(self.ObjList))
            # Iterate over the pool and return the first conflicted state
        while varPool:
            var = varPool.pop()
            if self.isConflicting(state, var):
                return var
        return -1   #Return this if there is no conflicted state

    def getNewState(self, state, var):
        """ select random position for the var 30 times, and check the position of minimum overlap.
            Returns the new state with the modified new position for var"""
        currentVar = state[var]
        localMinCount = currentVar[3]
        
        # if caught in local minimum, jump somewhere else
        if (localMinCount > 2):
            print "jump"
            if(var[1:]=='u'):
                state[var] = (random.uniform(self.valDomainUAV[0], self.valDomainUAV[1]), random.uniform(self.valDomainUAV[0], self.valDomainUAV[1]),self.UAVRadius,0)
            else:    
                state[var] = (random.uniform(self.valDomainBoat[0], self.valDomainBoat[1]), random.uniform(self.valDomainBoat[0], self.valDomainBoat[1]), self.boatRadius,0)
            localMinCount = 0
            
        minx = currentVar[0]
        miny = currentVar[1]
        minconflict = self.getTotalOverLap(state, var)
        
        origconflict = minconflict
        
        currx = minx
        curry = miny
        currConflict = minconflict
                
        for i in range(30):
            # Get new position
            if(var[1:]=='u'):
                currx = random.uniform(
                    max( (currx - currConflict * random.randrange(1, 4)), self.valDomainUAV[0] ),
                    min( (currx + currConflict * random.randrange(1, 4)), self.valDomainUAV[1] ) )
                curry = random.uniform(
                    max( (curry - currConflict * random.randrange(1, 4)), self.valDomainUAV[0] ),
                    min( (curry + currConflict * random.randrange(1, 4)), self.valDomainUAV[1] ) )
                state[var] = (currx, curry, self.UAVRadius, 0)
            else:
                currx = random.uniform(
                    max( (currx - currConflict * random.randrange(1, 4)), self.valDomainBoat[0] ),
                    min( (currx + currConflict * random.randrange(1, 4)), self.valDomainBoat[1] ) )
                curry = random.uniform(
                    max( (curry - currConflict * random.randrange(1, 4)), self.valDomainBoat[0] ),
                    min( (curry + currConflict * random.randrange(1, 4)), self.valDomainBoat[1] ) )
                state[var] = (currx, curry, self.boatRadius, 0)
            
            # measure conflict
            currConflict = self.getTotalOverLap(state, var)
            if(currConflict < minconflict):
                minx = currx
                miny = curry
                minconflict = currConflict
                localMinCount = 0
            if (currConflict == 0):
                break
         
        if (minconflict == origconflict):
            localMinCount = currentVar[3] + 1
        
        # set to minimum state
        state[var] = (minx, miny, currentVar[2], localMinCount)
        
        return state
        
    def getTotalOverLap(self, modState, var):
        totalOverLap=0
        for val in modState.keys():
            if val==var:
                continue
            totalOverLap += self.getOverlapDistance(modState[var],modState[val])
        return totalOverLap

    def visualize(self, state):
        """Visualize the current state by printing co-ordinates on the board"""
        for k,v in state.items():
            print k,v

############################################
    #TESTING
###########################################

# run with '-h' for 'usage'
import argparse
import random
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", choices=['AreaCoverage'], default='AreaCoverage', help="type of problem")
parser.add_argument("-n", type=int, default=8, help="environmental dimensions")
parser.add_argument("-m", type=int, default=3, help="number of uavs")
parser.add_argument("-o", type=int, default=2, help="radius of uavs")
parser.add_argument("-l", type=int, default=2, help="number of boats")
parser.add_argument("-k", type=int, default=1, help="radius of boats")
parser.add_argument("-t", type=int, default=10000, help="number of iterations")
parser.add_argument("-u", type=int, default=30, help="number of test cases for each iteration")
parser.add_argument("-s", type=int, default=None, help="seed")
args = parser.parse_args()

if args.p == "AreaCoverage":
    if (args.s == None):
        args.s = random.randint(0, sys.maxsize)
        print "seed = " + str(args.s)
    random.seed(args.s)
    prob = [AreaCoverage(args.n, args.m , args.o, args.l, args.k, args.u)]
    print 'AreaCoverage: n =', args.n

#state = prob.getStartState()

for p in prob:
    solveAgent.minConflict(p, args.t)

