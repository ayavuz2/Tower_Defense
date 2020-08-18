import pygame
import os
import math
from .tower import Tower


class ArcherTowerLong(Tower):
	def __init__(self, x, y):
		super().__init__(x, y)
		# self.tower_imgs = []
		self.archer_imgs = []
		self.archer_count = 0
		self.range = 200
		self.inRange = False

		# load archer tower imgs
		for x in range(4):
			self.tower_imgs.append(pygame.transform.scale(
				pygame.image.load(os.path.join("game_assets/towers/archer_towers/1", str(x) + ".png")), 
				(96, 96)))

		# load archer imgs
		for x in range(6): # change the archer img! 2000x1050 is too big to do proper scaling 
			self.archer_imgs.append(pygame.transform.scale(
				pygame.image.load(os.path.join("game_assets/towers/archer_towers/archer", str(x) + ".png")), 
				(96, 96)))

	def draw(self, win):
		# draw range circle
		surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA, 32)
		pygame.draw.circle(surface, (0,0,255, 128), (self.range, self.range), self.range, 0)

		win.blit(surface, (self.x - self.range, self.y - self.range))
		
		super().draw(win)

		if self.inRange:
			self.archer_count += 1
			if self.archer_count >= len(self.archer_imgs)*3:
				self.archer_count = 0
		else:
			self.archer_count = 0

		archer = self.archer_imgs[self.archer_count//3]
		win.blit(archer, ((self.x + self.width/2) - (archer.get_width()/2), (self.y - archer.get_height())))


	def change_range(self, r):
		"""
		change range of archer tower
		:param r: int
		:return: None
		"""
		self.range = r

	def attack(self, enemies):
		"""
		attacks an enemy in the enemy list, modifies list
		:param enemies: list of enemies
		:reurn: None
		"""
		self.inRange = False
		enemy_closest = []
		for enemy in enemies:
			x, y = enemy.x, enemy.y			

			dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
			if dis < self.range:
				self.inRange = True
				enemy_closest.append(enemy)
