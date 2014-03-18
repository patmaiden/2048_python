class Tile:
	def __init__(self,pos,val = 2):
		self.pos = pos

		self.value = val

		self.previousPos = None
		self.mergedFrom = None

	def x(self):
		return self.pos[0]

	def y(self):
		return self.pos[1]

	def savePosition(self):
		self.previousPos = self.pos

	def updatePosition(self, pos):
		self.pos = pos

	def __str__(self):
		return str(self.value)
