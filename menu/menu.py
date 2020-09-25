import pygame
import os
pygame.font.init()


coing_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "sell.png")), (35, 35))

class Button:
	"""
	Button class for menu object
	"""
	def __init__(self, x, y, img, name):
		self.x = x
		self.y = y
		self.name = name
		self.img = img
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	def click(self, X, Y):
		"""
		returns if the position has collided with the menu
		:param X: int
		:param Y: int
		:return: bool
		"""
		if X <= self.x + self.width and X >= self.x:
			if Y <= self.y + self.height and Y >= self.y:
				return True
		return False

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))


class Menu:
	"""
	menu for holding items
	"""
	def __init__(self, x, y, tower, img, item_cost):
		self.x = x
		self.y = y
		self.width = img.get_width()
		self.height = img.get_height()
		self.items = 0
		self.item_cost = item_cost
		self.buttons = []
		self.imgs = []
		self.menu_bg = img
		self.tower = tower
		self.font = pygame.font.SysFont("comicsans", 20)

	def draw(self, win):
		"""
		draws buttons and menu bg
		:param win: surface
		:retunr: None
		"""
		win.blit(self.menu_bg, (self.x - self.menu_bg.get_width()/2, self.y-120))
		for item in self.buttons:
			item.draw(win)
			win.blit(coing_img, (item.x + item.width + 20, item.y))
			text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255,255,255))
			win.blit(text, (item.x + item.width + 25, item.y + coing_img.get_height()))

	def add_button(self, img, name):
		"""
		adds buttons to menu
		:param img: surface
		:param name: str
		:return: None
		"""
		self.items += 1
		button_x = self.x - self.menu_bg.get_width()//2 + 15
		button_y = self.y - 120 + 15
		self.buttons.append(Button(button_x, button_y, img, name))

	def get_item_cost(self):
		"""
		gets cost of upgrade  to next level
		:return: int
		"""
		return self.item_cost[self.tower.level - 1]

	def get_clicked(self, X, Y):
		"""
		return the clicked item from the menu
		:param X: int
		:param Y: int
		:return: bool
		"""
		for button in self.buttons:
			if button.click(X,Y):
				return button.name

		return None
