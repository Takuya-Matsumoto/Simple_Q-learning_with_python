#!/usr/bin/python                                                           
# -*- coding:utf-8 -*-

import numpy as np
import sys

class Qlearning_Maze:
	"""Qlearning for Maze"""
	EPSILON = 0.30
	ALPHA = 0.10
	GAMMA = 0.90
	GOAL_REWARD = 100
	HIT_WALL_PENALTY = 5
	ONE_STEP_PENALTY = 1
	LEARNING_TIMES = 1000
	INIT_Q_MAX = 30
	MAZE = np.array(
			[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
			[0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
			[0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
			[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
			[0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
			[0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
			[0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
			[0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	)
	LEFT = 0
	UP = 1
	RIGHT = 2
	DOWN = 3

	def __init__(self):
		self.q = np.empty([10,10,4], int)
		self.sPosX = 1
		self.sPosY = 1
		self.sdPosX = 1
		self.sdPosY = 1
		self.route = []
		self.stepNum = int()

	def initAgent(self):
		self.sPosX = 1
		self.sPosY = 1
		self.stepNum = 0

	def eGreedy(self):
		selectedA = 0
		randNum = np.random.randint(0,100+1)

		if randNum <= self.EPSILON * 100.0 :
			for a in range(4):
				if self.q[self.sPosX][self.sPosY][selectedA] < self.q[self.sPosX][self.sPosY][a]:
					selectedA = a
		else :
			selectedA = np.random.randint(0,4);

		return selectedA

	def Action(self, direction):
		r = 0
		self.sdPosX = self.sPosX
		self.sdPosY = self.sPosY
		if direction == self.LEFT:
			if self.MAZE[self.sPosY][self.sPosX - 1] == 1:
				self.sdPosX = self.sdPosX - 1
			else:
				r = r - self.HIT_WALL_PENALTY
			route_str = "↑" + "[" + str(self.sdPosX) + "][" + str(self.sdPosY) + "]"
			self.route.append(route_str)
		elif direction == self.UP:
			if self.MAZE[self.sPosY - 1][self.sPosX] == 1:
				self.sdPosY = self.sdPosY - 1
			else:
				r = r - self.HIT_WALL_PENALTY
			route_str = "↑" + "[" + str(self.sdPosX) + "][" + str(self.sdPosY) + "]"
			self.route.append(route_str)
		elif direction == self.RIGHT:
			if self.MAZE[self.sPosY][self.sPosX + 1] == 1:
				self.sdPosX = self.sdPosX + 1
			else:
				r = r - self.HIT_WALL_PENALTY
			route_str = "↑" + "[" + str(self.sdPosX) + "][" + str(self.sdPosY) + "]"
			self.route.append(route_str)
		elif direction == self.DOWN:
			if self.MAZE[self.sPosY + 1][self.sPosX] == 1:
				self.sdPosY = self.sdPosY + 1
			else:
				r = r - self.HIT_WALL_PENALTY
			route_str = "↑" + "[" + str(self.sdPosX) + "][" + str(self.sdPosY) + "]"
			self.route.append(route_str)
		if self.sdPosX == 8 and self.sdPosY == 8 :
			r = self.GOAL_REWARD
		return r

	def initQ(self):
		for x in range(10):
			for y in range(10):
				for a in range(4):
					randNum = np.random.randint(0,self.INIT_Q_MAX + 1)
					self.q[x][y][a] = randNum


	def updateQ(self, r, a):
		maxA = 0
		for i in range(4):
			if self.q[self.sdPosX][self.sdPosY][maxA] < self.q[self.sdPosX][self.sdPosY][i]:
				maxA = i
		self.q[self.sPosX][self.sPosY][a] = (1.0 - self.ALPHA) * self.q[self.sPosX][self.sPosY][a] + self.ALPHA * ( r + self.GAMMA * self.q[self.sdPosX][self.sdPosY][maxA])

	def updateS(self):
		self.sPosX = self.sdPosX
		self.sPosY = self.sdPosY

	def printQ(self):
		for x in range(10):
			for y in range(10):
				for a in range(4):
					print "x:" + str(x) + " y:" + str(y) + " a:" + str(a) + " Q:" +str(self.q[x][y][a])
def main():
	minStepNum = sys.maxint
	learn = Qlearning_Maze()

	learn.initQ()
	for i in range(Qlearning_Maze.LEARNING_TIMES):
		learn.initAgent()
		learn.route = []
		Qlearning_Maze.isGoal = False
		while Qlearning_Maze.isGoal is False:
			learn.stepNum = learn.stepNum + 1
			a = learn.eGreedy()
			r = learn.Action(a)
			r = r - Qlearning_Maze.ONE_STEP_PENALTY
			learn.updateQ(r, a)
			learn.updateS()
			if learn.sPosX == 8 and learn.sPosY == 8 :
				Qlearning_Maze.isGoal = True
		if learn.stepNum < minStepNum :
			minStepNum = learn.stepNum
		if learn.stepNum == 22 :
			minStepNum = learn.stepNum
			learn.printQ()
			for j in range(len(learn.route)):
				print learn.route[j]
			print "学習回数:" + str(i) + " ゴールまでのステップ数:" + str(learn.stepNum) + " これまでの最小ステップ数:" + str(minStepNum)
			break
		print "学習回数:" + str(i) + " ゴールまでのステップ数:" + str(learn.stepNum) + " これまでの最小ステップ数:" + str(minStepNum)		


if __name__ == '__main__':
	main()