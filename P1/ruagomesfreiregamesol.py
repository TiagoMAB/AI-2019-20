import math
import pickle
import time

  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model =  model
    self.auxheur = auxheur
    pass

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    ##
    ## to implement
    ##
    if tickets == [math.inf, math.inf, math.inf]:
      print(init)
    print(tickets)
    return []
