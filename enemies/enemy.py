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
		self.path = [(40, 110), (331, 110), (631, 110), (831, 110), (831, 271), (128, 271), (128, 371), (128, 432), (831, 432), (831, 595), (400, 595), (40, 595), (-20, 595)]
		self.x = self.path[0][0]
		self.y = self.path[0][1]
		self.path_pos = 0
		self.img = None
		self.dis = 0
		self.move_count = 0
		self.move_dis = 0
		self.imgs = []
		self.flipped = False

	def draw(self, win):
		"""
		Draws the enemy with the given images
		:param win: surface
		:return: None
		"""
		self.img = self.imgs[self.animation_count]
		self.animation_count += 1

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

		if dirn[0] < 0 and not self.flipped:
			self.flipped = True
			for x, img in enumerate(self.imgs):
				self.imgs[x] = pygame.transform.flip(img, True, False)

		move_x, move_y = (self.x + dirn[0] * self.move_count, self.y + dirn[1] * self.move_count)
		self.dis += math.sqrt((move_x-x1)**2 + (move_y-y1)**2) # dis: distance

		self.x = move_x
		self.y = move_y

		# Go to next point
		if self.dis >= move_dis:
			self.dis = 0
			self.move_count = 0
			self.path_pos += 1
			if self.path_pos >= len(self.path):
				return False

		return True

	def hit(self):
		"""
		Returns if an enemy has died and removes one health for each call
		:return: None
		"""
		self.health -= 1
		if self.health <= 0:
			return True
