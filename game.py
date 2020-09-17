import pygame
import os
import time
import random
from enemies.scorpion import Scorpion
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import RangeTower, DamageTower
pygame.font.init()

lives_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "heart.png")), (48,48))


class Game:
	def __init__(self):
		self.width = 1100 # 1280
		self.height = 700 # 720
		self.win = pygame.display.set_mode((self.width, self.height))
		self.enemies = [Wizard()]
		self.attack_towers = [ArcherTowerLong(300,350)]
		self.support_towers = [RangeTower(500, 350)]
		self.lives = 10
		self.money = 100
		self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
		self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
		self.timer = time.time()
		self.life_font = pygame.font.SysFont("comicsans", 60)
		self.selected_tower = None

	def run(self):
		run = True
		clock = pygame.time.Clock()
				
		while run:
			clock.tick(30)

			if time.time() - self.timer >= random.randrange(2, 5)/2:
				self.timer = time.time()
				self.enemies.append(random.choice((Wizard(), Scorpion())))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				pos = pygame.mouse.get_pos()

				if event.type == pygame.MOUSEBUTTONDOWN:
					# look if you clicked on a attack tower

					button_clicked = None
					if self.selected_tower:
						button_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
						if button_clicked:
							print(button_clicked)

					if not button_clicked:
						for tw in self.attack_towers:
							if tw.click(pos[0], pos[1]):
								tw.selected = True
								self.selected_tower = tw
							else:
								tw.selected = False

						# look if you clicked on a support tower
						for tw in self.support_towers:
							if tw.click(pos[0], pos[1]):
								tw.selected = True
								self.selected_tower = tw
							else:
								tw.selected = False

			# loop through enemies
			to_del = []
			for en in self.enemies:
				if en.x < -5:
					to_del.append(en)

			# delete all enemies off the screen
			for d in to_del:
				self.lives -= 1
				self.enemies.remove(d)

			# loop through attack towers
			for tw in self.attack_towers:
				tw.attack(self.enemies)

			# loop through support towers
			for tw in self.support_towers:
				tw.support(self.attack_towers) # sending attack towers to see if they are in range of the support tower

			# if you lose
			if self.lives <= 0:
				print("You Lost")
				run = False

			self.draw()

		pygame.quit()

	def draw(self):
		self.win.blit(self.bg, (0,0))

		# draw attack towers
		for tw in self.attack_towers:
			tw.draw(self.win)
		
		# draw range towers
		for tw in self.support_towers:
			tw.draw(self.win)

		# draw enemies
		for en in self.enemies:
			en.draw(self.win)

		# draw lives
		text = self.life_font.render(str(self.lives), 1, (255,0,0))
		life = lives_img
		start_x = self.width - life.get_width() - 5

		self.win.blit(text, (start_x - text.get_width() - 10, 15))
		self.win.blit(life, (start_x, 10))

		pygame.display.update()

	def draw_menu(self):
		pass

g = Game()
g.run()
