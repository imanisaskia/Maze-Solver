# ---------- CLASSES ----------
class Vertex:
	def __init__(self, position):
		self.position = position	# tuple of (i,j)
	
class Edge:
	def __init__(self, source, target, weight):
		self.source = source		# index of source vertex
		self.target = target		# index of target vertex
		self.weight = weight		# steps taken from source to vertex [0...n]; 0 on source, n on target

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

	# prints source, target, and weight of every Edge
	def print(self):
		for i in self.data:
			print(i.source, '<->', i.target, '; weight =', i.weight)

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
def FindEdges(matrix, traveled, currentPos, source, steps):
	global Edges
	traveled.append(currentPos)
	vertexIndex = Vertices.findIndex(currentPos)

	i = currentPos[0]
	j = currentPos[1]

	if (vertexIndex != -999) and (vertexIndex != source):
		Edges.append(Edge(source, vertexIndex, steps))
	else:
		if (i+1 < N):
			if (matrix[i+1][j] == '0'):
				if ((i+1, j) not in traveled):
					FindEdges(matrix, traveled, (i+1, j), source, steps+1)
		if (i-1 >= 0):
			if (matrix[i-1][j] == '0'):
				if ((i-1, j) not in traveled):
					FindEdges(matrix, traveled, (i-1, j), source, steps+1)
		if (j+1 < M):
			if (matrix[i][j+1] == '0'):
				if ((i, j+1) not in traveled):
					FindEdges(matrix, traveled, (i, j+1), source, steps+1)
		if (j-1 >= 0):
			if (matrix[i][j-1] == '0'):
				if ((i, j-1) not in traveled):
					FindEdges(matrix, traveled, (i, j-1), source, steps+1)



# ---------- MAIN PROGRAM ----------
Matrix = []					# matrix from file
N = 0						# number of rows
M = 0						# number of columns

Vertices = VerticeArray()
'''
	index 0	-> entrance
	index 1 -> exit

	Vertices.len()				: returns length of array
	Vertices.append(Vertex)		: adds a new vertex to Vertices, duplicates are ignored
	Vertices.index(i)			: returns vertex at index i
	Vertices.findIndex((i,j))	: returns the index of vertex at position (i,j), or -999 if not found
	Vertices.print()			: prints list of vertices
'''

Edges = EdgeArray()
'''
	Edges.len()					: returns length of array
	Edges.append(Edge)			: adds a new edge to Edges, duplicates are ignored
	Edges.targetsFrom(i)		: returns a list of vertex indexes connected to vertex i
	Edges.print()				: prints list of edges
'''

Read("small.txt")
FindVertices(Matrix)
for i in range(Vertices.len()):
	FindEdges(Matrix, [], Vertices.index(i), i, 0)

# debug1
Vertices.print()
Edges.print()
