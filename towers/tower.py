import pygame
import os
import math
from menu.menu import Menu


menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu_horizontal.png")), (120, 70))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade.png")), (35, 35))

class Tower:
	"""
	Abstract class for towers
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = self.height = 96
		self.sell_price = [0,0,0]
		self.price = [0,0,0]
		self.level = 1
		self.range = 200
		self.original_range = self.range # Not sure if this should be in here
		self.selected = False
		# define menu and buttons
		self.menu = Menu(self.x, self.y, self, menu_bg, [2000, 5000, 9000, 12000, "MAX"])
		self.menu.add_button(upgrade_button, "Upgrade")
		self.moving = False
		self.tower_imgs = []
		self.damage = 1
		self.place_color = (0,0,255, 100)

	def draw(self, win):
		"""
		draws the tower
		:param win: surface
		:return: None
		"""
		img = self.tower_imgs[self.level - 1]
		win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

		# draw menu
		if self.selected:
			self.menu.draw(win)

	def draw_radius(self, win):
		# draw range circle if selected
		if self.selected:	
			surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA, 32)
			pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

			win.blit(surface, (self.x - self.range, self.y - self.range))

	def draw_placement(self, win):
		# draw range circle
		surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA, 32)
		pygame.draw.circle(surface, self.place_color, (58, 58), 58, 0) # 58 = 96/2 + 10

		win.blit(surface, (self.x - 58, self.y - 58))

	def click(self, X, Y):
		"""
		returns if tower has been clicked on
		and select tower if it was clicked
		:param X: int
		:param Y: int
		:return: bool
		"""
		img = self.tower_imgs[self.level - 1]
		if X  <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
			if Y <= self.y + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
				return True
		return False

	def sell(self):
		"""
		call to sell the tower, returns sel price
		:retutn: int
		"""
		return self.sell_price[self.level - 1]

	def upgrade(self):
		"""
		upgrades the tower for a given cost
		:return: None
		"""
		if self.level < len(self.tower_imgs):
			self.level += 1
			self.damage += 1

	def get_upgrade_cost(self):
		"""
		gets the upgrade cost
		:return: int
		"""
		return self.menu.get_item_cost()

	def move(self, x, y):
		"""
		moves tower to given x and y
		:param x: int
		:param y: int
		:return: None
		"""
		self.x = x
		self.y = y
		self.menu.x = x
		self.menu.y = y
		self.menu.update()

	def collide(self, otherTower):
		x2 = otherTower.x
		y2 = otherTower.y

		dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)

		return True if dis <= 116 else False # width and height of the towers are equals to 96 and adding 10 from both sides = 116
