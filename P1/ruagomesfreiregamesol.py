import math
import pickle
import time

class Node:

	def __init__(self, neighbours):
		self.visited = False
		self.h = 0
		self.neighbours = neighbours

class Graph:

	def __init__(self, goal, model):
		self.nodes = []
		
		for e in model[1:]:
			self.nodes.append(Node(e))
		
		if self.nodes[0].visited == False:
			print("Status: " + str(self.nodes[0].visited))
		self.goal = goal

	def bfs(self, goal, cost):
		self.nodes[goal].h = cost;

		queue = [goal] 				#maybe needs , after goal
		while len(queue) > 0:
			curr = queue[0]
			print("Curr:" + str(curr))
			self.nodes[curr].visited = True;

			for el in self.nodes[curr].neighbours:
				neighbour = el[1] - 1
				if self.nodes[neighbour].visited == False:
					queue.append(neighbour)
					self.nodes[neighbour].h = self.nodes[curr].h + 1
					self.nodes[neighbour].visited = True;

			queue.remove(curr)

	def printNode(self):
		size = len(self.nodes) + 1
		
		for i in range(1, size):
			print("Index: " + i + " h: " + self.nodes[i].h + " neighbours: " + self.nodes[i].neighbours)	
  
class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal = goal
		self.model =  model
		self.auxheur = auxheur
		self.graph = Graph(goal[0], model)
		self.graph.bfs(goal[0], 0)

		pass

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
		##
		## to implement
		##
		if tickets == [math.inf, math.inf, math.inf]:
			print(init)
			print(tickets)
		return []
