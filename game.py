from __future__ import division
import random
from time import sleep
from game_2048 import * 


DEBUG = True
def debug(*args):
	if DEBUG:
		print ' '.join(map(str, args))



class Game:
	def __init__(self, agent, level):
		self.agent = agent
		self.level = level
		self.total_reward = 0.0
		self.discounted_reward = 0.0
		self.moves = 0
		self.games = 0
		self.path_length = 0

	def run(self):

		state = self.level.grid.getState()
		iteration = 0
		discount = 1.0
		path_length = 0

		# moves = 0
		while True:
			print level.grid
			action = self.agent.get_action(state)
			reward, result, terminated, won = self.level.move(action)
			self.agent.update(state, action, reward, result)


			self.total_reward += reward
			self.discounted_reward += reward * discount
			discount *= gamma

			iteration += 1
			self.moves += 1
			path_length += 1
			state = result
			if won:
				debug('Success: reached end')
				debug('iterations/total:', '%d/%d' % (iteration, self.moves))
				debug('total reward:', int(round(self.total_reward)))
				debug('total discounted reward:', int(round(self.discounted_reward)))
				debug('')
				sleep(10)
				self.games += 1
				self.path_length = path_length+1
				self.level.setup()
				return True
			elif terminated:
				debug('Success: failed')
				debug('iterations/total:', '%d/%d' % (iteration, self.moves))
				debug('total reward:', int(round(self.total_reward)))
				debug('total discounted reward:', int(round(self.discounted_reward)))
				debug('')
				#sleep(0.5)
				self.games += 1
				self.path_length = path_length+1
				self.level.setup()
				return True
			sleep(0.01)
			# if self.moves > max_moves:
			# 	debug('Reached max_moves')
			# 	debug('iterations/total:', '%d/%d' % (iteration, self.moves))
			# 	debug('total reward:', int(round(self.total_reward)))
			# 	debug('total discounted reward:', int(round(self.discounted_reward)))
			# 	debug('')
			# 	self.games += 1
			# 	return False


class PendulumLevel:
	def __init__(self, plength, clenght):
		self.pendulum_length = plength
		self.cart_length = clength

	def is_fallen(self, state):
		return state

	def transition(self, state, action):
		if self.is_fallen(state):
			return 0, state, True

		(row,col) = state
		if random.random() < self.fall_prob(state):
			return 0, (state[0], 0), True
		else:
			direction = -1 if action == Action.left else 1
			return 1, (state[0] + direction , state[1] - direction), False




class Level:
	def __init__(self, squares):
		self.squares = squares
		self.rows = len(squares)
		self.cols = len(squares[0])
		self.goal_state = ("GOAL STATE",)

		for x in range(self.rows):
			for y in range(self.cols):
				if self.is_start((x,y)): self.start = (x,y)
				if self.is_end((x,y)): self.end = (x,y)

	@classmethod
	def load_level(cls, filename):
		squares = []
		for row in file(filename):
			squares.append(row.strip('\n'))
		return Level(squares)

	def is_ladder(self, state):
		(x,y) = state
		return self.squares[x][y] == "H"

	def is_floor(self, state):
		(x,y) = state
		return self.squares[x][y] in "_S"

	def is_gap(self, state):
		(x,y) = state
		return self.squares[x][y] == ' '

	def is_trapdoor(self, state):
		(x,y) = state
		return self.squares[x][y] in "123456789"

	def fall_prob(self, state):
		(x,y) = state
		if self.is_gap(state):
			return 1.0
		if self.is_trapdoor(state):
			return int(self.squares[x][y]) / 10.0
		else:
			return 0.0

	def is_start(self, state):
		(x,y) = state
		return self.squares[x][y] == 'S'

	def is_end(self, state):
		(x,y) = state
		return self.squares[x][y] == 'X'

	def is_goal_state(self, state):
		return state == self.goal_state

	def transition(self, state, action):
		# should never get here
		if self.is_goal_state(state):
			return 0, state, True

		(row,col) = state
		if random.random() < self.fall_prob(state):
			if row == self.rows - 1:
				raise ValueError("can't fall through bottom!")
			if gfx: gfx.player.fall()
			return 0, (row + 1, col), False
		else:
			if col == 0 and (action is Action.left or action is Action.jump_left):
				return -1, state, False
			if col == self.cols - 1 and (action is Action.right or action is Action.jump_right):
				return -1, state, False

			if col == 1 and action is Action.jump_left:
				return -1, state, False
			if col == self.cols - 2 and action is Action.jump_right:
				return -1, state, False


			if action is Action.left:
				if gfx: gfx.player.side(True, False)
				return -1, (row, col - 1), False
			if action is Action.jump_left:
				if gfx: gfx.player.side(True, True)				
				return -1, (row, col - 2), False
			if action is Action.right:
				if gfx: gfx.player.side(False, False)
				return -1, (row, col + 1), False
			if action is Action.jump_right:
				if gfx: gfx.player.side(False, True)
				return -1, (row, col + 2), False

			if action is Action.climb:
				if self.is_ladder(state):
					if gfx: gfx.player.climb()
					return -1, (row - 1, col), False
				if self.is_end(state):
					return 100, self.goal_state, True
				else:
					return -1, state, False



class Action:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

Action.left = Action("left")
Action.right = Action("right")
Action.jump_left = Action("jump left")
Action.jump_right = Action("jump right")
Action.climb = Action("climb")

Action.actions = [Action.left, Action.right, Action.jump_left, Action.jump_right, Action.climb]
Action.pendulum_actions = [Action.left, Action.right]

if __name__ == '__main__':
	from Agents import *
	import sys
	import argparse

	gamma = 0.9
	alpha = 0.1
	epsilon = 0.05

	level =  Game_2048(3, 512, None, None)

	#learner = Qlearner(alpha=alpha, gamma=gamma, actions=[0,1,2,3], epsilon=epsilon)
	learner = Rmax(rmax=512 + (level.size**2-1)*256, gamma=gamma, K=2,actions=[0,1,2,3])

	game = Game(learner, level)
	while game.run():
		pass

	#print 'total moves:', game.moves
	#print 'average discounted reward (gamma = %.3f): %d' % (gamma, int(round(game.discounted_reward / game.games)))
	#print 'optimal path length (according to learning algorithm):', game.path_length
	print '%d' % (int(round(game.discounted_reward / game.games)))
