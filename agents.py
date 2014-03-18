import random
from time import sleep
from collections import defaultdict
import math


class Agent:
	def __init__(self, game):
		this.game = game

	def makeMove(self):
		raise NotImplementedError()

class KeyInputAgent:
	def __init__(self):
		self.getch = _Getch()

	def makeMove(self):
		while(True):
			press = ord(self.getch())
			if press == 72: #up
				return 0
			elif press == 75: #left
				return 3
			elif press == 80: #down
				return 2
			elif press == 77: #right
				return 1
			elif press == 28 or press == 3:
				return	


class RandomAgent:
	def __init__(self, game):
		self.agme = game

	def get_action(self):
		sleep(0.2)
		return int(random.random()*4)





class Qlearner:
    Q = defaultdict(lambda:0)
    def __init__(self,alpha, gamma, actions, epsilon):
        assert type(epsilon)==float

        self.alpha = alpha # learning rate
        self.gamma = gamma # discount rate
        self.actions = actions
        self.epsilon = epsilon
    def update(self, s,a,r,s_):
        self.Q[s,a] = (1-self.alpha)*self.Q[s,a] + self.alpha*(r + self.gamma * max(self.Q[s_, a_] for a_ in self.actions))
    def get_action(self, s):
        # epsilon greedy
        if random.random() < self.epsilon:           
            # explore
            return random.choice(self.actions)
        else:
            # exploit
            return max(self.actions, key=lambda a: self.Q[s,a]) # argmax



class Rmax:
    def __init__(self, rmax, gamma, K, actions, iters=100):
        assert type(K)==int

        self.utopia = (None,None)
        self.count = defaultdict(float) # C[s,a]
        self.transition = defaultdict(float) # T[s,a,s_]
        self.reward = defaultdict(float) # R[s,a]

        self.rmax = rmax
        self.gamma = gamma
        self.K = K
        self.actions = actions
        self.iters = iters

        self.V  = defaultdict(float)
        self.V[self.utopia] = self.rmax

    def update(self, s,a,r,s_):
        # update(... s_) is always called before policy(... s_)
        self.count[s,a] += 1
        self.transition[s,a,s_] += 1
        self.reward[s,a] += r

        # value iteration
        if s not in self.V or self.count[s,a] == self.K:
            if s not in self.V: self.V[s] = 0.0
            converged = False
            while not converged:
                V_ = dict(self.V)
                converged = True
                for state in self.V:
                    self.V[state] = max(self.R(state,a) + self.gamma * sum(self.T(state,a,s2) * V_[s2]
                                                                           for s2 in V_)
                                        for a in self.actions)
                    if math.fabs(V_[state]) - math.fabs(self.V[state]) < -0.1 or math.fabs(V_[state]) - math.fabs(self.V[state]) > 0.1:
                        converged = False

    def R(self, s,a):
        if s == self.utopia: return self.rmax
        return 0.0 if self.count[s,a] < self.K else self.reward[s,a]/self.count[s,a]
    def T(self, s,a,s_):
        if self.count[s,a] < self.K:
            return 1.0 * (self.utopia == s_)
        else:
            return self.transition[s,a,s_]/self.count[s,a]
    def get_action(self, s):
        return max(self.actions, key=lambda a:
                       self.R(s,a) + self.gamma * sum(self.T(s,a,s_) * self.V[s_] for s_ in self.V))




"""KEYBOARD INPUT AND SUCH"""

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
        	self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        return msvcrt.getch()


