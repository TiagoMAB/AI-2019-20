import random
import math

class LearningAgent:

    def __init__(self,nS,nA):

        # define this function
        self.nS = nS
        self.nA = nA
        self.Q = [ [ -math.inf for i in range(nA) ] for j in range(nS) ]
        self.tM = 60

    def selectactiontolearn(self,st,aa):
        # define this function
        # print("select one action to learn better")

        r = random.randrange(100)
        if r > self.tM:
            a = 0
            for i in range(len(aa)):
                if (self.Q[st][i] > self.Q[st][a]):
                    a = i
        else:
            a = random.randrange(len(aa))
        return a

    # Select one action, used when evaluating
    # st - is the current state        
    # aa - is the set of possible actions
    # for a given state they are always given in the same order
    # returns
    # a - the index to the action in aa
    def selectactiontoexecute(self,st,aa):
        # define this function
        a = 0
        for i in range(len(aa)):
            if (self.Q[st][i] > self.Q[st][a]):
                a = i

        # print("select one action to see if I learned")
        return a

    def learn(self,ost,nst,a,r):
        # define this function
        #print("learn something from this data")
        alpha = 0.8 #check value
        y = 0.9#check value

        qMax = max(self.Q[nst])
        
        if self.Q[ost][a] == -math.inf:
            self.Q[ost][a] = alpha * ( r )
        else:
            self.Q[ost][a] = self.Q[ost][a] + alpha * ( r + y*qMax - self.Q[ost][a])
        
        return
