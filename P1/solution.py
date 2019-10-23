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
		self.f = depth * len(nodes)
		self.h = 0
		if anyorder:
			pass
		else:
			for i in range(len(nodes)):
				self.h += self.nodes[i].h[i]
		self.f += self.h
class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal = goal
		self.model =  model
		self.auxheur = auxheur
		self.limitexp = 0
		self.graph = Graph(model)
		self.graph.bfs(goal)
		#self.graph.printNode()

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
			
			if self.limitexp < 0:
				return []
			self.limitexp -= 1
		#	print(str(self.limitexp))
		#	print("Is this retarded» " + str(queue[0].f) + " Maybe? " + str(queue[0].depth * len(queue[0].nodes)))
			if queue[0].f == queue[0].depth * len(queue[0].nodes):
				print(self.limitexp)
				return queue[0].solution
				
			neighbours = []
			for n in queue[0].nodes:
				neighbours.append(n.neighbours)

			toAdd = list(itertools.product(*neighbours))
	#		if size == 1:
	#			print(str(toAdd))
			for el in toAdd:
				indexes = []
				nodes = []
				sol0 = []
				sol1 = []
				tickets = [] + queue[0].tickets
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
					sumTickets + t
					if t < 0: 
						valid = False
				
				if len(indexes) == len(set(indexes)) and valid and queue[0].depth <= limitdepth and (sumTickets == 0 or sumTickets >= len(nodes)):
		#			print(indexes)
					newstate = State(nodes, [] + queue[0].solution + [[sol0,sol1]], queue[0].depth + 1, tickets, anyorder)
					if result:
						print(self.limitexp)
						return newstate.solution
					#newstate.solution.append([sol0, sol1])
					queue.append(newstate)
					size += 1
					#print("Estado: " + str(newstate.solution) + "h: " + str(newstate.nodes[0].h) + "Depth: " + str(newstate.depth)+ "f: " + str(newstate.f))

			size -= 1	
			queue.pop(0)
			queue.sort(key = lambda state: (state.f, state.h) )
			#for i in queue:
		#		print("Death: " + str(i.solution) + "h: " + str(i.nodes[0].h) + "Depth: " + str(i.depth)+ "f: " + str(i.f))
			leeen = len(queue)
			while leeen > 2000:
				queue.pop(2000)
				leeen -= 1
				size -= 1	
		#print(str(neighbours))
		#print(str(queue))
		return []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):

		return self.algorithm(init, limitexp, limitdepth, tickets, anyorder)
