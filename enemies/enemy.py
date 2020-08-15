import pygame
import math


class Enemy:
	imgs = []

	def __init__(self):
		self.width = 64
		self.height = 64
		self.animation_count = 0
		self.health = 1
		self.vel = 3
		self.path = [(40, 110), (831, 110), (831, 271), (128, 271), (128, 432), (831, 433), (831, 595), (40, 596)]
		self.x = self.path[0][0]
		self.y = self.path[0][1]
		self.path_pos = 0
		self.img = None
		self.dis = 0
		self.move_count = 0
		self.move_dis = 0

	def draw(self, win):
		"""
		Draws the enemy with the given images
		:param win: surface
		:return: None
		"""
		self.animation_count += 1
		self.img = self.imgs[self.animation_count]
		
		if self.animation_count >= len(self.imgs):
			self.animation_count = 0

		win.blit(self.img, (self.x, self.y))
		self.move()

	def collide(self, X, Y):
		"""
		Returns if position has hit enemy
		:param x: int
		:param y: int
		:return: Bool
		"""
		if X <= self.x + self.width and X >= self.x:
			if Y <= self.y + self.height and Y >= self.y:
				return True
		return False

	def move(self):
		"""
		Move enemy
		:return: None
		"""
		x1, y1 = self.path[self.path_pos]
		if self.path_pos + 1 >= len(self.path):
			x2, y2 = (30, 596) # last pos in path x-10
		else:
			x2, y2 = self.path[self.path_pos+1]		

		move_dis = math.sqrt((x1-x1)**2 + (y2-y1)**2)

		self.move_count += 1
		dirn = (x2-x1, y2-y1)

		move_x, move_y = (self.x + dirn[0] * self.move_count, self.y + dirn[1] * self.move_count)
		self.dis += math.sqrt((move_x-x1)**2 + (move_y-y1)**2) # dis: distance

		# Go to next point
		if self.dis >= move_dis:
			self.dis = 0
			self.move_count = 0
			self.path_pos += 1

		self.x = move_x
		self.y = move_y

	def hit(self):
		"""
		Returns if an enemy has died and removes one health for each call
		:return: None
		"""
		self.health -= 1
		if self.health <= 0:
			return True
