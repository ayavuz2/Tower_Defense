import pygame
import os
from .tower import Tower


class ArcherTowerLong(Tower):
	def __init__(self, x, y):
		super().__init__(x, y)
		# self.tower_imgs = []
		self.archer_imgs = []
		self.archer_count = 0

		# load archer tower imgs
		for x in range(4):
			self.tower_imgs.append(pygame.transform.scale(
				pygame.image.load(os.path.join("game_assets/towers/archer_towers/1", str(x) + ".png")), 
				(96, 96)))

		# load archer imgs
		for x in range(6):
			self.archer_imgs.append(pygame.transform.scale(
				pygame.image.load(os.path.join("game_assets/towers/archer_towers/archer", str(x) + ".png")), 
				(32, 32)))

	def draw(self, win):
		super().draw(win)

		if self.archer_count >= len(self.archer_imgs):
			self.archer_count = 0

		archer = self.archer_imgs[self.archer_count]
		win.blit(archer, ((self.x + self.width/2) - (archer.get_width()/2), (self.y - archer.get_height())))

		self.archer_count += 1

	def attack(self, enemies):
		"""
		attacks an enemy in the enemy list, modifies list
		:param enemies: list of enemies
		:reurn: None
		"""
		pass