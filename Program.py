# ---------- CLASSES ----------
class Vertex:
	def __init__(self, position):
		self.position = position	# tuple of (i,j)
	
class Edge:
	def __init__(self, source, target, path):
		self.source = source		# index of source vertex
		self.target = target		# index of target vertex
		self.path = path			# path of (i,j) tuples from source to target
	
	def weight(self):
		return len(self.path)

class VerticeArray:
	def __init__(self):
		self.data = []
	def len(self):
		return len(self.data)

	# adds a new vertex to Vertices, duplicates are ignored
	def append(self, Vertex):
		found = False
		for i in self.data:
			if (i.position == Vertex.position):
				found == True
		if not found:
			self.data.append(Vertex)

	# returns position of vertex at index i
	def index(self, i):
		return self.data[i].position

	# returns index of vertex in position, or -999 if not found
	def findIndex(self, position):
		found = False
		index = 0
		for i in range(len(self.data)):
			if (self.data[i].position == position):
				found = True
				index = i
		if found:
			return index
		else:
			return -999
			
	# prints position of all Vertex
	def print(self):
		for i in range(len(self.data)):
			print(i, ':', self.data[i].position)

class EdgeArray:
	def __init__(self):
		self.data = []
	def len(self):
		return len(self.data)
	
	# adds new Edge if not yet added
	def append(self, Edge):
		found = False
		for i in self.data:
			if (i.source == Edge.source) and (i.target == Edge.target):
				found = True
			if (i.source == Edge.target) and (i.target == Edge.source):
				found = True
		if not found:
			self.data.append(Edge)

	# returns a list of vertex indexes connected to vertex index
	def targetsFrom(self, index):
		list = []
		for i in self.data:
			if (i.source == index):
				list.append(i.target)
			if (i.target == index):
				list.append(i.source)
		return list

	# return the weight of edge that connect currentidx to goalidx
	def findWeight(self, currentidx, goalidx):
		found=False
		i=0
		while(not(found) and i<len(self.data)):
			if(self.data[i].source == currentidx and self.data[i].target == goalidx):
				found=True
			else:
				i+=1
		if(not(found)):
			i=0
			while(not(found) and i<len(self.data)):
				if(self.data[i].target == currentidx and self.data[i].source == goalidx):
					found=True
				else:
					i+=1
		return 	self.data[i].weight()

	# return the path from source to target
	def findPath(self, currentidx, goalidx):
		found = False
		reverse = False
		i=0
		while(not(found) and i<len(self.data)):
			if(self.data[i].source == currentidx and self.data[i].target == goalidx):
				found = True
			else:
				i+=1
		if(not(found)):
			i=0
			while(not(found) and i<len(self.data)):
				if(self.data[i].target == currentidx and self.data[i].source == goalidx):
					found = True
					reverse = True
				else:
					i+=1
		if reverse:
			reversePath = self.data[i].path.copy()
			reversePath.reverse()
			return reversePath
		else:
			return self.data[i].path

	# prints source, target, and weight of every Edge
	def print(self):
		for i in self.data:
			print(i.source, '<->', i.target, '; weight =', i.weight())
			print(i.path)

# ---------- GLOBAL FUNCTIONS ----------
# reading matrix from file
def Read(source):
	global N, M, Matrix
	File = open(source, "r")
	N = len(File.readline()) - 1
	M = len(File.readlines()) + 1

	File.close()
	File = open(source, "r")

	for _ in range(N):
		Row = []
		for _ in range(M):
			Row.append(File.read(1))
		File.read(1)
		Matrix.append(Row)

# add all vertices
def FindVertices(matrix):
	global Vertices

	for i in range(N):
		if (matrix[i][0] == '0'):
			Vertices.append(Vertex((i, 0)))
		if (matrix[i][M-1] == '0'):
			Vertices.append(Vertex((i, M-1)))
	
	for i in range(1, N-1):
		for j in range(1, M-1):
			if (matrix[i][j] == '0'):
				path = 0
				if (matrix[i-1][j] == '0'):
					path = path + 1
				if (matrix[i+1][j] == '0'):
					path = path + 1
				if (matrix[i][j+1] == '0'):
					path = path + 1
				if (matrix[i][j-1] == '0'):
					path = path + 1
				if (path > 2):
					Vertices.append(Vertex((i,j)))

# add all edges from one vertex
def FindEdges(matrix, traveled, currentPos, source):
	global Edges

	newTraveled = traveled.copy()
	newTraveled.append(currentPos)
	vertexIndex = Vertices.findIndex(currentPos)

	i = currentPos[0]
	j = currentPos[1]

	if (vertexIndex == source):
		down = '1'
		up = '1'
		right = '1'
		left = '1'

		if (i+1 < N):
			down = matrix[i+1][j]
		if (i-1 >= 0):
			up = matrix[i-1][j]
		if (j+1 < M):
			right = matrix[i][j+1]
		if (j-1 >= 0):
			left = matrix[i][j-1]

		if (down == '0') and ((i+1, j) not in traveled):
			FindEdges(matrix, newTraveled, (i+1, j), source)
		if (up == '0') and ((i-1, j) not in traveled):
			FindEdges(matrix, newTraveled, (i-1, j), source)
		if (right == '0') and ((i, j+1) not in traveled):
			FindEdges(matrix, newTraveled, (i, j+1), source)
		if (left == '0') and ((i, j-1) not in traveled):
			FindEdges(matrix, newTraveled, (i, j-1), source)

	elif (vertexIndex != -999) and (vertexIndex != source):
		Edges.append(Edge(source, vertexIndex, newTraveled))
	
	else:
		down = '1'
		up = '1'
		right = '1'
		left = '1'

		if (i+1 < N):
			down = matrix[i+1][j]
		if (i-1 >= 0):
			up = matrix[i-1][j]
		if (j+1 < M):
			right = matrix[i][j+1]
		if (j-1 >= 0):
			left = matrix[i][j-1]

		if (down == '0') and ((i+1, j) not in traveled):
			FindEdges(matrix, newTraveled, (i+1, j), source)
		elif (up == '0') and ((i-1, j) not in traveled):
			FindEdges(matrix, newTraveled, (i-1, j), source)
		elif (right == '0') and ((i, j+1) not in traveled):
			FindEdges(matrix, newTraveled, (i, j+1), source)
		elif (left == '0') and ((i, j-1) not in traveled):
			FindEdges(matrix, newTraveled, (i, j-1), source)
					
# ---------- A STAR ----------

# return third element of list
def takeFormula(elem):
	return elem[2]

# return linear distance from vertex to goal h(n) 
def distance(vertex,goal):
	return math.sqrt(((vertex[0]-goal[0])**2) + ((vertex[1]-goal[1])**2))

#AStar	
def AStar(VerticeArray, EdgeArray, aStarSolution):
	prioqueue = [] 		#prioqueue : current vertex, solution list, f(n), actualcost (g(n))
	prioqueue.append([Vertices.findIndex(Vertices.index(0)), [], 0, 0]) #append entrance

	final=False
	#ambil elemen pertama di prioqueue, cek solusi bukan
	#untuk setiap elemen x di prioqueue hitung nilai f(n) edge (misal ke simpul y) : actualcost i + g(n) x ke y + h(n) dari y ke goal
	#urutkan di prioqueue berdasarkan f(n)
	#ulangi hingga solusi
	while(not(final)):
		if (prioqueue[0][0] == 1):
			final=True
			for j in prioqueue[0][1]:
				aStarSolution.append(j)
			aStarSolution.append(prioqueue[0][0])
		else:										#first element in prioqueue isn't exit
			solution = prioqueue[0][1].copy()
			solution.append(prioqueue[0][0])
			for i in EdgeArray.targetsFrom(prioqueue[0][0]):
				if(not(i in prioqueue[0][1])):
					actualcost = prioqueue[0][3] + (EdgeArray.findWeight(prioqueue[0][0],i))	#g(n)
					fn = actualcost + distance(VerticeArray.index(i),VerticeArray.index(1)) 	#f(n) = g(n) + h(n)
					prioqueue.append([i, solution, fn, actualcost])
			prioqueue.pop(0)
			prioqueue.sort(key=takeFormula)	#sort prioqueue by f(n)

# ---------- BFS ----------
def BFS(VerticeArray, EdgeArray, BFSSolution):
	queue = [] 		#queue : simpul hidup, list solusi
	queue.append([Vertices.findIndex(Vertices.index(0)),[]]) #append entrance

	dikunjungi = []
	for i in VerticeArray.data:
		dikunjungi.append(0)

	final=False
	#ambil elemen pertama di queue, cek solusi bukan
	#untuk setiap elemen x di queue, ekspan lalu taruh di queue
	#ulangi hingga solusi
	while(not(final)):
		if (queue[0][0] == 1):
			final=True
			for j in queue[0][1]:
				BFSSolution.append(j)
			BFSSolution.append(queue[0][0])
		else:										#first element in queue isn't exit
			dikunjungi[queue[0][0]]=1
			solution = queue[0][1].copy()
			solution.append(queue[0][0])
			for i in EdgeArray.targetsFrom(queue[0][0]):
				if(dikunjungi[i]==0):
					queue.append([i, solution])
			queue.pop(0)

# create a path tracing a list of vertices
def TraceRoute(vertices):
	route = []
	for i in range(len(vertices) - 1):
		temp = Edges.findPath(vertices[i], vertices[i+1])
		for j in temp:
			route.append(j)
	return route

# generate visualization of maze and path using PyGame
def Visualize(matrix, a_star, bfs):
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((N*15, M*15))
	pygame.display.set_caption("Maze Solver :D")
	clock = pygame.time.Clock()

	for i in range(N):
		for j in range(M):
			if (Matrix[i][j] == '0'):
				color = (255,255,255)
			else:
				color = (0,0,0)

			pygame.draw.rect(screen, color, (j*15, i*15, 15, 15), 0)
			pygame.display.update()

	wait = True
	while wait:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				wait = False

	color = (0,200,0)
	for step in bfs:
		i = step[0]
		j = step[1]
		pygame.draw.circle(screen, color, (j*15 + 7, i*15 + 7), 5, 0)
		pygame.display.update()
		clock.tick(50)

	wait = True
	while wait:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				wait = False

	color = (50,50,255)
	for step in a_star:
		i = step[0]
		j = step[1]
		pygame.draw.circle(screen, color, (j*15 + 7, i*15 + 7), 5, 0)
		pygame.display.update()
		clock.tick(50)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.quit()
				quit()

# ---------- MAIN PROGRAM ----------
import math
import pygame
from pygame.locals import *
import os

Matrix = []					# matrix from file
N = 0						# number of rows
M = 0						# number of columns
Vertices = VerticeArray()
Edges = EdgeArray()

source = input("External file: ")

Read(source)
FindVertices(Matrix)
for i in range(Vertices.len()):
	FindEdges(Matrix, [], Vertices.index(i), i)

aStarSolution = []	#A* solution list
AStar(Vertices, Edges, aStarSolution)

BFSSolution = []	#BFS solution list
BFS(Vertices, Edges, BFSSolution)

# visualization
aStarRoute = TraceRoute(aStarSolution)
BFSRoute = TraceRoute(BFSSolution)

Visualize(Matrix, aStarRoute, BFSRoute)