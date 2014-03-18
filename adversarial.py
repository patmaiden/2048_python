import math 
import game
import copy


class agent:
	def __init__(self, game):
		self.game = game
		self.lastFrobidden = False

	def makeMove(self):
		return self.find_best_move(6,6,self.game, 3)

	def find_best_move(self, depth, top_depth,game, dir):
		if depth == 0:
			return dir
		if self.lastFrobidden:
			self.lastFrobidden = False
			return 1
		best_score = -10000
		best_action = 3
		allowed = [0,1,2]
		for x in allowed:
			movedCopy = copy.deepcopy(game)
			movedCopy.move(x)
			best_dir_to_here = self.find_best_move(depth-1,top_depth,movedCopy, x)
			if not self.gridsEqual(movedCopy.grid, game.grid):
				if self.eval(movedCopy) > best_score:
					best_score = self.eval(movedCopy)
					best_action = x
		if best_action == 3 and depth == top_depth:
			self.lastFrobidden = True
		return best_action

	def eval(self, game):
		return game.grid.maxValue()*10 + len(game.grid.availableCells())*2 if game.grid.maxValueInCorner() else game.grid.maxValue() + len(game.grid.availableCells())*2

	def gridsEqual(self, grid1, grid2):
		list1 = grid1.eachCell()
		list2 = grid2.eachCell()
		for i in xrange(len(list1)):
			if list1[i] != None and list2[i] != None and list1[i].value == list2[i].value:
				continue
			elif list1[i] == None and list2[i] == None:
				continue
			else:
				return False
		return True
