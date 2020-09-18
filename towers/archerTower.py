import pygame
import os
import math
import time
from .tower import Tower


tower_imgs1 = []
archer_imgs1 = []
# load archer tower imgs
for x in range(4):
	tower_imgs1.append(pygame.transform.scale(
		pygame.image.load(os.path.join("game_assets/towers/archer_towers/1", str(x) + ".png")), 
		(96, 96)))


class ArcherTowerLong(Tower):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.tower_imgs = tower_imgs1[:]
		self.archer_imgs = archer_imgs2[:]
		self.archer_total_imgs = len(archer_imgs2)
		self.archer_count = 0
		self.range = 200
		self.original_range = self.range
		self.original_damage = self.damage
		self.inRange = False
		self.left = True
		self.damage = 1
		self.animation_speed_multiplier = 2
		self.width = self.height = 90

	def draw(self, win):
		super().draw_radius(win)
		super().draw(win)

		if self.inRange:
			self.archer_count += 1
			if self.archer_count >= len(self.archer_imgs)*self.animation_speed_multiplier:
				self.archer_count = 0
		else:
			self.archer_count = 0

		archer = self.archer_imgs[self.archer_count//self.animation_speed_multiplier]
		win.blit(archer, (self.x  - (archer.get_width()/2), (self.y - archer.get_height() - 20)))

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

		enemy_closest.sort(key = lambda x: x.x)
		if len(enemy_closest) > 0:
			first_enemy = enemy_closest[0]

			if self.archer_count == 9:
				if first_enemy.hit(self.damage) == True:
					enemies.remove(first_enemy)

			if first_enemy.x < self.x and not self.left:
				self.left = True
				for x, img in enumerate(self.archer_imgs):
					self.archer_imgs[x] = pygame.transform.flip(img, True, False)
			
			elif first_enemy.x > self.x and self.left:
				self.left = False
				for x, img in enumerate(self.archer_imgs):
					self.archer_imgs[x] = pygame.transform.flip(img, True, False)

		def flip_archer_imgs(self): # no need atm.
			pass	


tower_imgs2 = []
archer_imgs2 = []

# load archer tower imgs
for x in range(3):
	tower_imgs2.append(pygame.transform.scale(
		pygame.image.load(os.path.join("game_assets/towers/archer_towers/2", str(x) + ".png")),
		(96, 96)))

# load archer imgs
for x in range(10):
	if x != 6:
		archer_imgs2.append(pygame.transform.scale(
			pygame.image.load(os.path.join("game_assets/towers/archer_towers/archers/archer_2", str(x) + ".png")), 
			(48, 64)))
	else:
		archer_imgs2.append(pygame.transform.scale(
			pygame.image.load(os.path.join("game_assets/towers/archer_towers/archers/archer_2", str(x) + ".png")), 
			(128, 64)))

class ArcherTowerShort(ArcherTowerLong):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.tower_imgs = tower_imgs2[:]
		self.archer_imgs = archer_imgs2[:]
		self.archer_total_imgs = len(archer_imgs2)
		self.archer_count = 0
		self.range = 100
		self.inRange = False
		self.original_range = self.range
		self.original_damage = self.damage
		self.left = True
		self.damage = 2
		self.animation_speed_multiplier = 2
