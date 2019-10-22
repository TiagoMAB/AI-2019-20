import math
import pickle
import time

class Node:

	def __init__(self, h, pathcost, index, neighbours, state, depth, tickets):
		self.visited = False
		self.h = h
		self.pathcost = pathcost
		self.f = sum(self.h) + self.pathcost
		self.neighbours = neighbours
		self.index = index
		self.state = state
		self.depth = depth
		self.tickets = tickets

class Graph:

	def __init__(self, model):
		self.nodes = []
		size = len(model)
		
		for i in range(1, size):
			self.nodes.append(Node([], 0, i, model[i], [[[], [i]]], 0, [0, 0, 0]))

	def bfs(self, goal):
		
		for g in goal:
			self.nodes[g- 1].h.append(0)

			queue = [g - 1]
			while len(queue) > 0:
				curr = queue[0]
				self.nodes[curr].visited = True

				for el in self.nodes[curr].neighbours:
					neighbour = el[1] - 1
					if self.nodes[neighbour].visited == False:
						queue.append(neighbour)
						self.nodes[neighbour].h.append(self.nodes[curr].h[-1] + 1)
						self.nodes[neighbour].visited = True

				queue.remove(curr)
			for n in self.nodes:
				n.visited = False


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
		self.graph = Graph(model)
		self.graph.bfs(goal)
		self.graph.printNode()

	def algorithm(self, position, limitexp, limitdepth, transport):

		queue = []
		self.limitexp = limitexp - 1
		numAgents = len(position)
        
		for p in position:
			curr = self.graph.nodes[p - 1]
			curr.tickets = transport
			new = Node(curr.h, 0, curr.index, curr.neighbours, curr.state, curr.depth, curr.tickets)
			queue.append(new)

		size = 1
		while size > 0:
			size -= 1
			self.limitexp -= 1

			if self.limitexp < 0:
				return []
			
			if queue[0].h[0] == 0:
				return queue[0].state
			
			for el in queue[0].neighbours:
				neighbour = self.graph.nodes[el[1] - 1]
				node = Node(neighbour.h, queue[0].pathcost + numAgents, neighbour.index, neighbour.neighbours, queue[0].state + [[[el[0]],[el[1]]]], queue[0].depth + 1, [] + queue[0].tickets)
				node.tickets[el[0]] -= 1
				if node.tickets[0] >= 0 and node.tickets[1] >= 0 and node.tickets[2] >= 0 and node.h == 0:	#possible optimization, checking for solution while generating nodes, may encounter an error because we are checking limitexpansions at the beginning
					return node.state
				if node.tickets[0] >= 0 and node.tickets[1] >= 0 and node.tickets[2] >= 0 and node.depth <= 10:
					queue.append(node)
					size += 1
			queue.pop(0)
			queue.sort(key = lambda node: node.f)
	
		#	size = len(queue)
		#	for i in range(0, size):
		#		print("Index1: " + str(queue[i].index) + " | h: " + str(queue[i].h) + " | neighbours: " + str(queue[i].neighbours))
		#	print(" ---")
		return []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
		
		result = self.algorithm(init, limitexp, limitdepth, tickets)

		return result
