import pygame
import os
import math
import time
from .tower import Tower


# Find a way to make code do not check support function every second.
# Maybe do it by a check statement if it is already effected by the support towers or not

range_imgs = [(pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets/towers/support_towers/range_tower", "{}.png").format(i)),
	 (96,128))) for i in range(2)]


class RangeTower(Tower):
	"""
	Add extra range to each surrounding tower
	"""
	def __init__(self, x, y):
		super().__init__(x, y)
		self.name = "range_Tower"
		self.range = 200
		self.original_range = self.range
		self.effect = [0.2, 0.4]
		self.effected_towers = []
		self.tower_imgs = range_imgs[:]
		self.width = self.height = 96

	def draw(self, win):
		super().draw_radius(win)
		super().draw(win)

	def support(self, towers):
		"""
		will modify towers according to ability
		:param towers: list
		:return: None
		"""
		for tower in towers:
			x, y = tower.x, tower.y			
			dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)

			if dis <= self.range + tower.width/2:
				if tower not in self.effected_towers:
					self.effected_towers.append(tower)

		for tower in self.effected_towers:
			tower.range = tower.original_range + round(tower.original_range * self.effect[self.level - 1])


damage_imgs = [(pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets/towers/support_towers/damage_tower", "{}.png").format(i)),
	 (128,128))) for i in range(2)]


class DamageTower(RangeTower):
	"""
	Add damage to surrounding towers
	"""
	def __init__(self, x, y):
		super().__init__(x, y)
		self.name = "damage_Tower"
		self.range = 200
		self.original_range = self.range
		self.effect = [1, 2]
		self.effected_towers = []
		self.tower_imgs = damage_imgs[:]
		self.width = self.height = 96

	def support(self, towers):
		"""
		will modify towers according to ability
		:param towers: list
		:return: None
		"""
		for tower in towers:
			x, y = tower.x, tower.y			
			dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)

			if dis <= self.range + tower.width/2:
				if tower not in self.effected_towers:
					self.effected_towers.append(tower)

		for tower in self.effected_towers:
			tower.damage = tower.original_damage + self.effect[self.level - 1]
