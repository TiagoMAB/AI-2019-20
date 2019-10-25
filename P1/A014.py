# Grupo 14 - Daniel Pereira nº89425 - Tiago Barroso nº89549

import math
import pickle
import time
import itertools

class Node:

	def __init__(self, h, index, neighbours):
		self.visited = False
		self.h = h
		self.neighbours = neighbours
		self.index = index

class Graph:

	def __init__(self, model):
		self.nodes = []
		size = len(model)
		
		for i in range(1, size):
			self.nodes.append(Node([], i, model[i]))

	def bfs(self, goal):
		
		# Executes a BFS starting in each goal
		# Calculates a heuristic's value for each node (and for each goal)
		# The heuristic function is the depth of the node in the BFS
		for g in goal:
			self.nodes[g- 1].h.append(0)

			queue = [g - 1]
			while len(queue) > 0:
				curr = self.nodes[queue[0]]				
				curr.visited = True

				for el in curr.neighbours:
					neighbour = el[1] - 1
					if self.nodes[neighbour].visited == False:
						queue.append(neighbour)
						self.nodes[neighbour].h.append(curr.h[-1] + 1)
						self.nodes[neighbour].visited = True

				queue.pop(0)
			for n in self.nodes:
				n.visited = False

class State:

	def __init__(self, nodes, solution, depth, tickets, anyorder):
		self.nodes = nodes
		self.solution = solution
		self.depth = depth 
		self.tickets = tickets
		self.f = depth
		self.h = 0

		# When anyorder == false the heuristic's value of the state will be the biggest value 
		# of self.nodes[i].h[i] in which "i" is goes up to the number of goals
		# When anyorder == true we call self.getH() to determine the value
		if anyorder:
			self.h += self.getH()
		else:
			for i in range(len(nodes)):
				if self.nodes[i].h[i] > self.h:
					self.h = self.nodes[i].h[i]
		self.f += self.h

	def getH(self):

		# Calculates the heuristic value based on the minimum of a list
		# of possible values
		lst = []
		for n in self.nodes:
			lst = lst + [n.h]
		
		indexes = []
		length = len(lst)
		for i in range(0, length):
			indexes = indexes + [i]

		perm = itertools.permutations(indexes)
		
		h = math.inf
		for p in perm:
			currH = 0
			j = 0
			for i in p:
				if lst[j][i] > currH:
					currH = lst[j][i]
				j += 1
			if currH < h:
				h = currH

		return h

class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal = goal
		self.model =  model
		self.auxheur = auxheur
		self.limitexp = 0
		self.graph = Graph(model)
		self.graph.bfs(goal)

	def algorithm(self, position, limitexp, limitdepth, transport, anyorder):

		queue = []
		self.limitexp = limitexp - 1

		ls = []

		for p in position:
			ls.append(self.graph.nodes[p - 1])
		
		state = State(ls, [[[], position]], 0, transport, anyorder)
		queue.append(state)
		size = 1

		while size > 0:

			current = queue[0]
			queue.pop(0)
			size -= 1

			if self.limitexp < 0:
				return []

			self.limitexp -= 1
	
			if current.f == current.depth:
				return current.solution
				
			neighbours = []
			for n in current.nodes:
				neighbours.append(n.neighbours)
				
			toAdd = list(itertools.product(*neighbours))

			for el in toAdd:
				indexes = []
				sol0 = []
				sol1 = []
				tickets = [] + current.tickets
				result = True
				i = 0
		
				#Prepares initialization of neighbour state and checks if it is a solution
				for n in el:
					indexes.append(n[1] - 1)
					if self.graph.nodes[n[1] - 1].h[i] != 0:
						result = False
					tickets[n[0]] -= 1
					sol0.append(n[0])
					sol1.append(n[1])
					i += 1

				#Checks if state is valid based on the tickets available
				valid = True
				sumTickets = 0
				for t in tickets:
					sumTickets += t
					if t < 0: 
						valid = False
				
				#If conditions are met, the state is placed in a queue to apply the algorithm
				if len(indexes) == len(set(indexes)) and valid and current.depth <= limitdepth:

					nodes = []
					for i in indexes:
						nodes.append(self.graph.nodes[i])
						
					newstate = State(nodes, [] +current.solution + [[sol0,sol1]], current.depth + 1, tickets, anyorder)

					if result:
						return newstate.solution

					if sumTickets >= len(nodes):
						queue = [newstate] + queue
						size += 1

			queue.sort(key = lambda state: state.f )

			length = len(queue)
			while length > self.limitexp:
				queue.pop(self.limitexp)
				length -= 1
				size -= 1	

		return []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):

		return self.algorithm(init, limitexp, limitdepth, tickets, anyorder)