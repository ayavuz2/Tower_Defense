import pygame
import os
pygame.font.init()


coin_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "sell.png")), (35, 35))
coin_img2 = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "sell.png")), (15, 15))


class Button:
	"""
	Button class for menu object
	"""
	def __init__(self, menu, img, name):
		self.menu = menu
		self.x = menu.x - self.menu.menu_bg.get_width()/2 + 15
		self.y = menu.y - 105
		self.name = name
		self.img = img
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	def draw(self, win):
		"""
		draws the button image
		:param win: surface
		:return: None
		"""
		win.blit(self.img, (self.x, self.y))

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

	def update(self):
		"""
		updates button position
		:return: None
		"""
		self.x = self.menu.x - self.menu.menu_bg.get_width()/2 + 15
		self.y = self.menu.y - 105 # 120 - 15


class VerticalButton(Button):
	"""
	Button class for menu object
	"""
	def __init__(self, x, y, img, name, cost):
		self.x = x
		self.y = y
		self.name = name
		self.img = img
		self.width = self.img.get_width()
		self.height = self.img.get_height()
		self.cost = cost


class PlayPauseButton(Button):
	def __init__(self, play_img, pause_img, x, y):
		self.img = pause_img
		self.play = play_img
		self.pause = pause_img
		self.x = x
		self.y = y
		self.width = self.img.get_width()
		self.height = self.img.get_height()
		self.paused = True

	def draw(self, win):
		if self.paused:
			win.blit(self.play, (self.x, self.y))
		else:
			win.blit(self.pause, (self.x, self.y))

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
		win.blit(self.menu_bg, (self.x - self.menu_bg.get_width()/2, self.y - 120))
		for item in self.buttons:
			item.draw(win)
			win.blit(coin_img, (item.x + item.width + 20, item.y))
			text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255,255,255))
			win.blit(text, (item.x + item.width + 25, item.y + coin_img.get_height()))

	def add_button(self, img, name):
		"""
		adds buttons to menu
		:param img: surface
		:param name: str
		:return: None
		"""
		self.items += 1
		# button_x = self.x
		# button_y = self.y
		self.buttons.append(Button(self, img, name))

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

	def update(self):
		"""
		update button location
		:return: None
		"""
		for button in self.buttons:
			button.update()


class VerticalMenu(Menu):
	"""
	Vertical Menu for side bar of game
	"""
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.width = img.get_width()
		self.height = img.get_height()
		self.items = 0
		self.buttons = []
		self.imgs = []
		self.menu_bg = img
		self.font = pygame.font.SysFont("comicsans", 20)

	def draw(self, win):
		"""
		draws buttons and menu bg
		:param win: surface
		:retunr: None
		"""
		win.blit(self.menu_bg, (self.x - self.width/2, self.y))
		for item in self.buttons:
			item.draw(win)
			win.blit(coin_img2, (item.x, item.y + item.height + 3))
			text = self.font.render(str(item.cost), 1, (255,255,255))
			win.blit(text, (item.x + coin_img2.get_width() + 3, item.y + item.height + 5))

	def add_button(self, img, name, cost):
		"""
		adds buttons to menu
		:param img: surface
		:param name: str
		:return: None
		"""
		self.items += 1
		button_x = self.x - 20
		button_y = self.y + 25 + (self.items - 1) * 90
		self.buttons.append(VerticalButton(button_x, button_y, img, name, cost))	

	def get_item_cost(self, name):
		"""
		gets the cost of the item
		:param name: str
		:return: int
		"""
		for button in self.buttons:
			if button.name == name:
				return button.cost
		return -1
