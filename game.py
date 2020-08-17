import pygame
import os
from enemies.scorpion import Scorpion
from enemies.wizard import Wizard


class Game:
	def __init__(self):
		self.width = 1100
		self.height = 700
		self.win = pygame.display.set_mode((self.width, self.height))
		self.enemies = [Scorpion(), Wizard()]
		self.towers = []
		self.lives = 10
		self.money = 100
		self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
		self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

	def run(self):
		run = True
		clock = pygame.time.Clock()
		
		while run:
			clock.tick(30)
			# pygame.time.delay(50)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				pos = pygame.mouse.get_pos()
				print(pos)

				if event.type == pygame.MOUSEBUTTONDOWN:
					pass

			# loop through enemies
			to_del = []
			for en in self.enemies:
				if en.x < -5:
					to_del.append(en)

			# delete all enemies off the screen
			for d in to_del:
				self.enemies.remove(d)

			self.draw()

		pygame.quit()

	def draw(self):
		self.win.blit(self.bg, (0,0))

		# draw enemies
		for en in self.enemies:
			en.draw(self.win)

		pygame.display.update()


g = Game()
g.run()