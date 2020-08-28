import pygame
import os
import math
import time
from .tower import Tower



tower_imgs = []
archer_imgs1 = []
# load archer tower imgs
for x in range(4):
	tower_imgs.append(pygame.transform.scale(
		pygame.image.load(os.path.join("game_assets/towers/archer_towers/1", str(x) + ".png")), 
		(96, 96)))

# load archer imgs
for x in range(6): # change the archer img! 2000x1050 is too big to do proper scaling 
	archer_imgs1.append(pygame.transform.scale(
		pygame.image.load(os.path.join("game_assets/towers/archer_towers/archers/archer_1", str(x) + ".png")), 
		(96, 96)))

class ArcherTowerLong(Tower):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.tower_imgs = tower_imgs[:]
		self.archer_imgs = archer_imgs1[:]
		self.archer_count = 0
		self.range = 200
		self.inRange = False
		self.left = False
		self.timer = time.time()
		self.damage = 1

	def draw(self, win):
		# draw range circle
		surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA, 32)
		pygame.draw.circle(surface, (128,128,128, 100), (self.range, self.range), self.range, 0)

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

		enemy_closest.sort(key = lambda x: x.x)
		if len(enemy_closest) > 0:
			first_enemy = enemy_closest[0]

			if time.time() - self.timer >= 0.5:
				self.timer = time.time()
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


archer_imgs2 = []
# load archer imgs
for x in range(6): 
	archer_imgs2.append(pygame.transform.scale(
		pygame.image.load(os.path.join("game_assets/towers/archer_towers/archers/archer_2", str(x) + ".png")), 
		(96, 96)))


class ArcherTowerShort(ArcherTowerLong):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.tower_imgs = tower_imgs[:]
		self.archer_imgs = archer_imgs2[:]
		self.archer_count = 0
		self.range = 100
		self.inRange = False
		self.left = False
		self.timer = time.time()
		self.damage = 2
