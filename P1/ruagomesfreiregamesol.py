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

class State:

	def __init__(self, nodes, solution, depth, tickets, anyorder):
		self.nodes = nodes
		self.solution = solution
		self.depth = depth 
		self.tickets = tickets
		self.f = depth
		self.h = 0
		if anyorder:
			self.h += self.getH()
			pass
		else:
			for i in range(len(nodes)):
				if self.nodes[i].h[i] > self.h:
					self.h = self.nodes[i].h[i]
		self.f += self.h

	def getH(self):

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
		visitedindexes = []
		while size > 0:
			counter = 0
			iii = []
			for c in queue[0].nodes:
				iii.append(c)
			visitedindexes.append([iii])
			if self.limitexp < 0:
				return []
			self.limitexp -= 1
	
			if queue[0].f == queue[0].depth:
				print(self.limitexp)
				return queue[0].solution
				
			neighbours = []
			for n in queue[0].nodes:
				neighbours.append(n.neighbours)
				
			toAdd = list(itertools.product(*neighbours))

			for el in toAdd:
				indexes = []
				nodes = []
				sol0 = []
				sol1 = []
				tickets = [] + queue[counter].tickets
				result = True
				i = 0
				for n in el:
					indexes.append(n[1] - 1)
					nodes.append(self.graph.nodes[n[1] - 1])
					if self.graph.nodes[n[1] - 1].h[i] != 0:
						result = False
					tickets[n[0]] -= 1
					sol0.append(n[0])
					sol1.append(n[1])
					i += 1

				valid = True
				sumTickets = 0
				for t in tickets:
					sumTickets += t
					if t < 0: 
						valid = False
				
				if len(indexes) == len(set(indexes)) and valid and queue[counter].depth <= limitdepth:

					newstate = State(nodes, [] + queue[counter].solution + [[sol0,sol1]], queue[counter].depth + 1, tickets, anyorder)

					if result:
						print(self.limitexp)
						return newstate.solution

					if sumTickets >= len(nodes):
						queue = [newstate] + queue
						size += 1
						counter += 1

			size -= 1	
			queue.pop(counter)
			queue.sort(key = lambda state: state.f )

			length = len(queue)
			while length > self.limitexp:
				queue.pop(self.limitexp)
				length -= 1
				size -= 1	

		return []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):

		return self.algorithm(init, limitexp, limitdepth, tickets, anyorder)