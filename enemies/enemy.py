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
		self.path = [(40, 110), (331, 110), (631, 110), (925, 110), (925, 271), (128, 271), (128, 371), (128, 432), (831, 432), (831, 595), (400, 595), (40, 595), (-20, 595)]
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

		win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
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
			x2, y2 = (-10, 596)
		else:
			x2, y2 = self.path[self.path_pos+1]		

		move_dis = math.sqrt((x2-x1)**2 + (y2-y1)**2)

		dirn = (x2-x1, y2-y1)
		length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
		dirn = ((dirn[0])/length, (dirn[1])/length)

		if dirn[0] < 0 and not self.flipped:
			self.flipped = True
			for x, img in enumerate(self.imgs):
				self.imgs[x] = pygame.transform.flip(img, True, False)

		move_x, move_y = (self.x + dirn[0], self.y + dirn[1])
		self.dis += length

		self.x = move_x
		self.y = move_y

		# Go to next point
		if dirn[0] >= 0: # moving right
			if dirn[1] >= 0: # moving down
				if self.x >= x2 and self.y >= y2:
					self.path_pos += 1
			else: # moving up
				if self.x >= x2 and self.y <= y2:
					self.path_pos += 1
		else: # moving left
			if dirn[1] >= 0: # moving down
				if self.x <= x2 and self.y >= y2:
					self.path_pos += 1
			else: # moving up 
				if self.x <= x2 and self.y <= y2:
					self.path_pos += 1

	def hit(self):
		"""
		Returns if an enemy has died and removes one health for each call
		:return: None
		"""
		self.health -= 1
		if self.health <= 0:
			return True
