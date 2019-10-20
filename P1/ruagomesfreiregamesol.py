import math
import pickle
import time

class Node:

	def __init__(self, h, index, neighbours, state, depth):
		self.visited = False
		self.h = h
		self.neighbours = neighbours
		self.index = index
		self.state = state
		self.depth = depth

class Graph:

	def __init__(self, goal, model):
		self.nodes = []
		size = len(model)
		
		for i in range(1, size):
			self.nodes.append(Node(0, i, model[i], [[[], [i]]], 0))

	def bfs(self, goal, cost):
		self.nodes[goal- 1].h = cost

		queue = [goal - 1] 				#maybe needs , after goal
		while len(queue) > 0:
			curr = queue[0]
	#		print("Curr:" + str(curr))
			self.nodes[curr].visited = True

			for el in self.nodes[curr].neighbours:
				neighbour = el[1] - 1
				if self.nodes[neighbour].visited == False:
					queue.append(neighbour)
					self.nodes[neighbour].h = self.nodes[curr].h + 1
					self.nodes[neighbour].visited = True

			queue.remove(curr)

	def printNode(self):
		size = len(self.nodes)
		
		for i in range(0, size):
			print("Index: " + str(i + 1) + " | h: " + str(self.nodes[i].h) + " | neighbours: " + str(self.nodes[i].neighbours))	
  
class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal = goal
		self.model =  model
		self.auxheur = auxheur
		self.limitexp = 0
		self.graph = Graph(goal[0], model)
		self.graph.bfs(goal[0], 0)
		#self.graph.printNode()
		pass

	def algorithm(self, position, limitdepth, transport):

#		if limitdepth == 0 or self.limitexp == 0:
#			return []
#		if self.graph.nodes[position].h == 0:
#			return 
		result = []
		queue = [] 
		curr = self.graph.nodes[position - 1]
		self.limitexp -= 1

		for el in curr.neighbours:
			neighbour = self.graph.nodes[el[1] - 1]
			node = Node(neighbour.h, neighbour.index, neighbour.neighbours, curr.state + [[[el[0]],[el[1]]]], curr.depth + 1)
			queue.append(node)
			

		queue.sort(key = lambda node: node.h)
		size = len(queue)
		
	#	for i in range(0, size):
	#		print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours))

		while len(queue) > 0:
			if queue[0].h == 0:
				return queue[0].state
			for el in queue[0].neighbours:
				neighbour = self.graph.nodes[el[1] - 1]
				node = Node(neighbour.h, neighbour.index, neighbour.neighbours, queue[0].state + [[[el[0]],[el[1]]]], queue[0].depth + 1)
				queue.append(node)
	#			for i in range(0, size):
	#				print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours))
			queue.sort(key = lambda node: node.h)
			

		size = len(queue)
		
	#	for i in range(0, size):
	#		print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours))


		return []


	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
		##
		## to implement
		##

#		if tickets == [math.inf, math.inf, math.inf]:
#			print(init)
#			print(tickets)


		result = self.algorithm(init[0], limitdepth, [])
		return result
