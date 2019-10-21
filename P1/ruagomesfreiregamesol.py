import math
import pickle
import time

class Node:

	def __init__(self, h, index, neighbours, state, depth, tickets):
		self.visited = False
		self.h = h
		self.neighbours = neighbours
		self.index = index
		self.state = state
		self.depth = depth
		self.tickets = tickets

class Graph:

	def __init__(self, goal, model):
		self.nodes = []
		size = len(model)
		
		for i in range(1, size):
			self.nodes.append(Node(0, i, model[i], [[[], [i]]], 0, [0, 0, 0]))

	def bfs(self, goal, cost):
		self.nodes[goal- 1].h = cost

		queue = [goal - 1]
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

	def algorithm(self, position, limitexp, limitdepth, transport):

#		if limitdepth == 0 or self.limitexp == 0:
#			return []
#		if self.graph.nodes[position].h == 0:
#			return 
		queue = []
		curr = self.graph.nodes[position - 1]
		self.limitexp = limitexp - 1
		#if transport != [math.inf,math.inf,math.inf]:
		curr.tickets = [] + transport
		print("Tickets: " + str(transport))

		for el in curr.neighbours:
			neighbour = self.graph.nodes[el[1] - 1]
			node = Node(neighbour.h, neighbour.index, neighbour.neighbours, curr.state + [[[el[0]],[el[1]]]], curr.depth + 1, [] + curr.tickets)
			node.tickets[el[0]] -= 1	
			if node.tickets[0] >= 0 and node.tickets[1] >= 0 and node.tickets[2] >= 0:
				queue.append(node)
		
		queue.sort(key = lambda node: node.h)
		size = len(queue)
		
		print("Tickets: " + str(transport))
		for i in range(0, size):
			print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours) + " | tickets: " + str(queue[i].tickets))

		while size > 0:
			print("Index: " + str(queue[0].index) + "Tickets: " + str(queue[0].tickets))
			self.limitexp -= 1
			if queue[0].h == 0:
				return queue[0].state

			if self.limitexp == 2000:
				return []
			
			if queue[0].depth <= 10:
				for el in queue[0].neighbours:
					neighbour = self.graph.nodes[el[1] - 1]
					node = Node(neighbour.h, neighbour.index, neighbour.neighbours, queue[0].state + [[[el[0]],[el[1]]]], queue[0].depth + 1, [] + queue[0].tickets)
					node.tickets[el[0]] -= 1
					if node.tickets[0] >= 0 and node.tickets[1] >= 0 and node.tickets[2] >= 0 and node.h == 0:
						return node.state
					if node.tickets[0] >= 0 and node.tickets[1] >= 0 and node.tickets[2] >= 0:
						queue.append(node)
				queue.pop(0)
				queue.sort(key = lambda node: node.h)	
	
		#	size = len(queue)
		#	for i in range(0, size):
		#		print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours))
		#	print(" ---")
		return []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
		
		result = self.algorithm(init[0], limitexp, limitdepth, tickets)
		return result
