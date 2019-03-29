# ---------- CLASSES ----------
class Vertex:
	def __init__(self, position):
		self.position = position
	
class Edge:
	def __init__(self, source, target, weight):
		self.source = source
		self.target = target
		self.weight = weight

class VerticeArray:
	def __init__(self):
		self.data = []
	def len(self):
		return len(self.data)

	# adds new Vertex if not yet added
	def append(self, Vertex):
		found = False
		for i in self.data:
			if (i.position == Vertex.position):
				found == True
		if not found:
			self.data.append(Vertex)
	
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
				found == True
		if not found:
			self.data.append(Edge)
	
	# prints source, target, and weight of every Edge
	def print(self):
		for i in self.data:
			print(i.source, '->', i.target, '; weight =', i.weight)

# ---------- GLOBAL VARIABLES ----------
Matrix = []
N = 0
M = 0
Entrance = ()
Exit = ()
Vertices = VerticeArray()
Edges = EdgeArray()

# ---------- GLOBAL FUNCTIONS ----------
# reading matrix from file
def Read(source):
	global N, M
	File = open(source, "r")
	N = len(File.readline()) - 1
	M = len(File.readlines()) + 1

	File.close()
	File = open(source, "r")

	for i in range(N):
		Row = []
		for j in range(M):
			Row.append(File.read(1))
		File.read(1)
		Matrix.append(Row)

# finding the positions of entrance and exit
def FindEntranceExit(matrix):
	global Entrance, Exit, Vertices

	for i in range(N):
		if (matrix[i][0] == '0'):
			Entrance = (i, 0)
		if (matrix[i][M-1] == '0'):
			Exit = (i, (M-1))
	
	Vertices.append(Vertex(Entrance))
	Vertices.append(Vertex(Exit))



# ---------- MAIN PROGRAM ----------
Read("small.txt")
FindEntranceExit(Matrix)
Vertices.print()