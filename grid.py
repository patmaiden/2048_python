class Grid:
	def __init__(self, size):
		self.size = size
		self.cells = []

		self.build()

	"""Constructs empty grid"""
	def build(self):
		for x in xrange(self.size):
			self.cells.append(list())

			for y in xrange(self.size):
				self.cells[-1].append(None)

	def randomAvailableCell(self):
		import random
		return random.choice(self.availableCells())

	"""returns set of unoccupied cells as a list of tuples"""
	def availableCells(self):
		toRet = []
		for x in xrange(self.size):
			for y in xrange(self.size):
				if self.cells[x][y] == None:
					toRet.append((x,y))
		return toRet

	def eachCell(self):
		toRet = []
		for x in self.cells:
			for y in x:
				toRet.append(y)
		return toRet

	def getState(self):
		toRet = []
		for x in self.cells:
			for y in x:
				if y != None:
					toRet.append(y.value)
				else:
					toRet.append(y)
		return tuple(toRet)

	def cellsAvailable(self):
		for x in self.cells:
			for y in x:
				if y == None:
					return True
		return False

	def cellAvailable(self, cell):
		return self.cells[cell[0]][cell[1]] == None

	def cellOccupied(self, cell):
		return self.cells[cell[0]][cell[1]] != None

	def cellContent(self, cell):
		if self.withinBounds(cell):
			return self.cells[cell[0]][cell[1]]
		return None

	"""tile will be an object"""
	def insertTile(self, tile):
		self.cells[tile.x()][tile.y()] = tile
	
	def removeTile(self, tile):
		self.cells[tile.x()][tile.y()] = None

	def withinBounds(self, position):
		return position[0]>= 0 and position[0] < self.size and position[1]>= 0 and position[1] < self.size


	def maxValue(self):
		return max([x.value for x in self.eachCell() if x != None]) if max([x.value for x in self.eachCell() if x != None]) != 2048 else 100000000

	def maxValueInCorner(self):
		maxVal = self.maxValue()
		#print (self.cellContent((0,0)) != None and self.cellContent((0,0)).value == maxVal) or (self.cellContent((self.size-1,0)) != None and self.cellContent((self.size-1,0)).value == maxVal) or (self.cellContent((0,self.size-1)) != None and self.cellContent((0,self.size-1)).value == maxVal) or (self.cellContent((self.size-1,self.size-1)) != None and self.cellContent((self.size-1,self.size-1)).value == maxVal)
		return (self.cellContent((0,0)) != None and self.cellContent((0,0)).value == maxVal) or (self.cellContent((self.size-1,0)) != None and self.cellContent((self.size-1,0)).value == maxVal) or (self.cellContent((0,self.size-1)) != None and self.cellContent((0,self.size-1)).value == maxVal) or (self.cellContent((self.size-1,self.size-1)) != None and self.cellContent((self.size-1,self.size-1)).value == maxVal)

	"""prints grid in nice format"""
	def __str__(self):
		toRet = ""
		for x in xrange(self.size):
			for y in xrange(self.size):
				if self.cells[y][x] == None:
					toRet += 'X' + "  "
				else:
					toRet += str(self.cells[y][x]) + "  "
			toRet += '\n'
		return toRet


