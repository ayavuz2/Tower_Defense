import pygame
import os
import math
import time
from .tower import Tower


range_imgs = [(pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets/towers/support_towers/range_tower", "{}.png").format(i)),
	 (64, 64))) for i in range(2)]

class RangeTower(Tower):
	"""
	Add extra range to each surrounding tower
	"""
	def __init__(self, x, y):
		super().__init__(x, y)
		self.radius = 150
		self.effect = [0.2, 0.4]
		self.imgs = range_imgs

	def draw(self, win):
		super().draw_radius(win)
		super().draw(win)

	def support(self, towers):
		"""
		will modify towers according to ability
		:param towers: list
		:return: None
		"""
		pass


damage_imgs = [(pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets/towers/support_towers/damage_tower", "{}.png").format(i)),
	 (64, 64))) for i in range(2)]

class DamageTower(RangeTower):
	"""
	Add damage to surrounding towers
	"""
	def __init__(self):
		super().__init__(x, y)
		self.radius = 150
		self.effect = [1, 2]
		self.imgs = damage_imgs

	def support(self, towers):
		"""
		will modify towers according to ability
		:param towers: list
		:return: None
		"""
		pass
