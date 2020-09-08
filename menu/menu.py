import pygame
import os

menu_bg = pygame.image.load(os.path.join("game_assets", "menu.png"))

class Button:
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name
		self.img = None
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
		if Y >= self.y + self.height and Y >= self.y:
			return True
	return False

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))


class Menu:
	"""
	menu for holding items
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 0
		self.height = 0
		self.item_names = []
		self.items = 0
		self.buttons = []
		self.imgs = []

	def draw(self, win):
		"""
		draws buttons and menu bg
		:param win: surface
		:retunr: None
		"""
		for button in self.buttons:
			button.draw(win)

	def add_button(self, img, name):
		"""
		adds buttons to menu
		:param img: surface
		:param name: str
		:return: None
		"""
		self.items += 1
		increment_x = self.width/self.items/2
		button_x = self.items * increment_x - img.get_width()/2
		button_y = self.y + self.get_height/2 - img.get_height()/2
		self.buttons.append(Button(button_x, button_y, name))

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
