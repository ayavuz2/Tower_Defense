import pygame
import os


class Button:
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
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.width = img.get_width()
		self.height = img.get_height()
		self.item_names = []
		self.items = 0
		self.buttons = []
		self.imgs = []
		self.menu_bg = img

	def draw(self, win):
		"""
		draws buttons and menu bg
		:param win: surface
		:retunr: None
		"""
		win.blit(self.menu_bg, (self.x - self.menu_bg.get_width()/2, self.y-120))
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
		# increment_x = self.width/self.items/2
		button_x = self.x - self.menu_bg.get_width()//2 + 15
		button_y = self.y - 120 + 15
		self.buttons.append(Button(button_x, button_y, img, name))

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
