from grid import Grid
from tile import Tile
from agents import *
import math

class Game_2048:
	def __init__(self,size,win_score, Actuator, ScoreManager):
		self.size = size
		self.actuator = Actuator
		self.scoreManager = ScoreManager
		self.win_score = win_score
		self.startTiles = 2

		self.setup()

	def setup(self):
		self.grid = Grid(self.size)#to-do - implement this

		self.score = 0
		self.over = False
		self.won = False

		self.addStartTiles()


	def addStartTiles(self):
		for i in xrange(self.startTiles):
			self.addRandomTile()

	def addRandomTile(self):
		import random
		if self.grid.cellsAvailable():
			value = 2
			if random.random() < 0.1:
				value = 4
			tile = Tile(self.grid.randomAvailableCell(), value)

			self.grid.insertTile(tile)

	def actuate(self):
		pass

	def prepareTiles(self):
		for x in self.grid.eachCell():
			if x != None:
				x.mergedFrom = None
				x.savePosition()

	def moveTile(self, tile, cell):
		self.grid.cells[tile.x()][tile.y()] = None
		self.grid.cells[cell[0]][cell[1]] = tile
		tile.updatePosition(cell)

	def move(self, direction):
		if self.won or self.over:
			return

		cell = None
		tile = None



		vector = self.vectorMap(direction)
		traversals = self.buildTraverals(vector)
		moved = False

		self.prepareTiles()


		for x in traversals['x']:
			for y in traversals['y']:
				cell = (x,y)
				tile = self.grid.cellContent(cell)
				if(tile != None):
					positions = self.findFarthestPosition(cell,vector)
					next = self.grid.cellContent(positions['next'])

					if(next != None and next.value == tile.value and next.mergedFrom == None):
						merged = Tile(positions['next'], tile.value*2)
						merged.mergedFrom = [tile, next]

						self.grid.insertTile(merged)
						self.grid.removeTile(tile)
						tile.updatePosition(positions['next'])

						self.score += merged.value

						if (merged.value == self.win_score):
							sleep(10)
							self.won = True
					else:
						self.moveTile(tile, positions['farthest'])

						if (not self.positionsEqual(cell, tile)):
							moved = True
		if moved:
			self.addRandomTile()

			if not self.movesAvalable():
				self.over = True				

			self.actuate()

	def buildTraverals(self, vector):
		traversals = {'x': [], 'y': []}
		for pos in xrange(self.size):
			traversals['x'].append(pos)
			traversals['y'].append(pos)
		if vector[0] == 1:
			traversals['x'].reverse()
		if vector[1] == 1:
			traversals['y'].reverse()
		return traversals

	def findFarthestPosition(self, cell, vector):
		previous = cell
		cell = (previous[0] + vector[0], previous[1] + vector[1])
		while (self.grid.withinBounds(cell) and self.grid.cellAvailable(cell)):
			previous = cell
			cell = (previous[0] + vector[0], previous[1] + vector[1])
		return {'farthest': previous, 'next': cell}



	def movesAvalable(self):
		return self.grid.cellsAvailable() or self.tileMatchesAvailable()

	def tileMatchesAvailable(self):
		tile = None

		for x in xrange(self.size):
			for y in xrange(self.size):
				tile = self.grid.cellContent((x,y))
				if (tile != None):
					for direction in xrange(4):
						vector = self.vectorMap(direction)
						cell = (x + vector[0], y + vector[1])

						other = self.grid.cellContent(cell)

						if(other != None and other.value == tile.value):
							return True
		return False

	def positionsEqual(self,cell,tile):
		return cell[0] == tile.x() and cell[1] == tile.y()

	def vectorMap(self,direction):
		if direction == 0:
			return (0,-1)
		elif direction == 1:
			return (1,0)
		elif direction == 2:
			return (0,1)
		elif direction == 3:
			return (-1,0)
		else:
			raise NotImplementedError()


	def maxValue(self):
		return max([x.value for x in self.grid.eachCell() if x != None])

	def smoothness(self):
		smoothness = 0
		for x in xrange(self.size):
			for y in xrange(self.size):
				if self.grid.cellOccupied((x,y)):
					value = math.log(self.cellContent(x,y).value)
					for direction in xrange(1,3):
						vector = self.vectorMap(direction)
						targetCell = self.findFarthestPosition((x,y), vectorMap)['next']

						if self.grid.cellOccupied(targetCell):
							target = self.cellOccupied(targetCell)
							targetValue = math.log(target.value)/math.log(2)
							smoothness -= math.fabs*value - targetValue
		return smoothness

	def monotonicity2(self):
		totals = [0,0,0,0]

		for x in xrange(self.size):
			current = 0
			next = current + 1
			while next < 4:
				while next < 4 and not self.grid.cellOccupied((x,next)):
					next += 1
				if next >- 4:
					next -= 1
				currentValue =  math.log(self.cellContent((x,current)).value) / math.log(2) if self.cellOccupied(x,current) else 0
				nextValue = math.log(self.cellContent((x,next)).value) / math.log(2) if self.cellOccupied(x,next) else 0
				if currentValue > nextValue:
					totals[0] += nextValue - currentValue
				elif nextValue > currentValue:
					totals[1] += currentValue - nextValue
				current = next
				next += 1

		for y in xrange(self.size):
			current = 0
			next = current + 1
			while next < 4:
				while next < 4 and not self.grid.cellOccupied((next,y)):
					next += 1
				if next >- 4:
					next -= 1
				currentValue =  math.log(self.cellContent((current,y)).value) / math.log(2) if self.cellOccupied(current,y) else 0
				nextValue = math.log(self.cellContent((next,y)).value) / math.log(2) if self.cellOccupied(next,y) else 0
				if currentValue > nextValue:
					totals[2] += nextValue - currentValue
				elif nextValue > currentValue:
					totals[3] += currentValue - nextValue
				current = next
				next += 1
		return max(totals[0],totals[1]) + max(totals[2],totals[3])


if __name__ == "__main__":
	from adversarial import agent
	g = Game_2048(4,2048,None,None)
	a = agent(g)
	print g.grid
	while (not (g.won or g.over)):
		direction = a.makeMove()
		if direction == None:
			break
		g.move(direction)
		print g.grid

