import pygame


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
		self.imgs = []

	def click(self, x, y):
		pass
