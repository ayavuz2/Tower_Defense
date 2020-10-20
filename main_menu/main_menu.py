import pygame
import os
from game import Game
from menu.menu import Button
pygame.font.init()

start_button = pygame.image.load(os.path.join("game_assets", "start_button.png"))


class MainMenu:
	def __init__(self):
		self.width = 1366
		self.height = 768
		self.win = pygame.display.set_mode((self.width, self.height))
		
		self.button = (self.width/2 - start_button.get_width()//2, self.height/2 - start_button.get_height()//2,
			start_button.get_width(), start_button.get_height())
		self.font = pygame.font.SysFont("comicsans", 50)
		self.bg = pygame.transform.scale(
			pygame.image.load(os.path.join("game_assets", "menu_bg.png")), (self.width, self.height))

	def run(self):
		run = True

		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.MOUSEBUTTONUP:
					# check if hit start button
					x, y = pygame.mouse.get_pos()

					if self.button[0] <= x <= self.button[0] + self.button[2]:
						if self.button[1] <= y <= self.button[1] + self.button[3]:
							game = Game(self.win)
							game.run()
							del game

			self.draw()

		pygame.quit()

	def draw(self):
		self.win.blit(self.bg, (0, 0))
		self.win.blit(start_button, (self.button[0], self.button[1]))

		text = self.font.render("PLAY", 1, (255,255,255))
		self.win.blit(text, (self.button[0] + start_button.get_width()//2 - text.get_width()//2,
			self.button[1] + start_button.get_height()//2 - text.get_height()//2))

		pygame.display.update()
		
