import pygame
import os
import time
import random
from enemies.scorpion import Scorpion
from enemies.wizard import Wizard
from enemies.club import Club
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu
pygame.font.init()


lives_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "heart.png")), (48,48))
coin_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "sell.png")), (35, 35))

side_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "menu_vertical.png")), (80, 400))

buy_archer = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "buy_archer.png")), (45, 45))
buy_archer2 = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "buy_archer2.png")), (45, 45))
buy_damage = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "buy_damage.png")), (45, 45))
buy_range = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "buy_range.png")), (45, 45))

attack_tower_names = ["archer_Tower", "archer_Tower2"]
support_tower_names = ["damage_Tower", "range_Tower"]

# waves are in form
# frequency of enemies
# (# scorpions, # wizards, # club)
waves = [
	[10, 0, 0],
	[20, 0, 0],
	[30, 0, 0],
	[40, 0, 0],
	[30, 10, 0],
	[20, 20, 0],
	[10, 30, 0],
	[10, 40, 0],
	[20, 40, 0],
	[30, 30, 5],
	[0, 40, 10],
	[0, 30, 20],
	[10, 20, 30],
	[0, 0, 40],
	[40, 40, 40]
]


class Game:
	def __init__(self):
		self.width = 1100 # 1280
		self.height = 700 # 720
		self.win = pygame.display.set_mode((self.width, self.height))
		self.enemies = []
		self.attack_towers = [ArcherTowerLong(300,350)]
		self.support_towers = [DamageTower(300, 500)]
		self.lives = 10
		self.money = 2000
		self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
		self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
		self.timer = time.time()
		self.life_font = pygame.font.SysFont("comicsans", 50)
		self.selected_tower = None
		self.pause = False
		self.wave = 0
		self.current_wave = waves[self.wave][:]
		self.moving_object = None
		self.menu = VerticalMenu(self.width - side_img.get_width() + 30, 140, side_img)
		self.menu.add_button(buy_archer, "buy_archer", 500)
		self.menu.add_button(buy_archer2, "buy_archer2", 700)
		self.menu.add_button(buy_damage, "buy_damage", 1000)
		self.menu.add_button(buy_range, "buy_range", 1000)

	def run(self):
		run = True
		clock = pygame.time.Clock()
				
		while run:
			clock.tick(30)

			if self.pause == False:
				# gen monsters
				if time.time() - self.timer >= random.randrange(2, 5)/2:
					self.timer = time.time()
					self.gen_enemies()

			pos = pygame.mouse.get_pos()

			# check for moving object
			if self.moving_object:
				self.moving_object.move(pos[0], pos[1])

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					# if you are moving an object and click
					if self.moving_object:

						if self.moving_object.name in attack_tower_names:
							self.attack_towers.append(self.moving_object)
							print("Done")

						elif self.moving_object.name in support_tower_names:
							self.support_towers.append(self.moving_object)
						
						# self.moving_object.x = pos
						self.moving_object.moving = False
						self.moving_object = None

					else:
						# look if you click on side menu
						side_menu_button = self.menu.get_clicked(pos[0], pos[1])
						if side_menu_button:
							cost = self.menu.get_item_cost(side_menu_button)
							if self.money >= cost:
								self.money -= cost
								self.add_tower(side_menu_button)

						# look if you clicked on a attack tower or support tower
						button_clicked = None
						if self.selected_tower:
							button_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
							if button_clicked:
								if button_clicked == "Upgrade":
									cost = self.selected_tower.get_upgrade_cost()
									if self.money >= cost:
										self.money -= cost
										self.selected_tower.upgrade()

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
				self.money += tw.attack(self.enemies)

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

		# draw moving object
		if self.moving_object:
			self.moving_object.draw(self.win)

		# draw menu
		self.menu.draw(self.win)

		# draw lives
		text = self.life_font.render(str(self.lives), 1, (255,0,0))
		life = lives_img
		start_x = self.width - life.get_width() - 5

		self.win.blit(text, (start_x - text.get_width() - 10, 15))
		self.win.blit(life, (start_x, 10))

		# draw money
		text = self.life_font.render(str(self.money), 1, (255,255,0))
		money = pygame.transform.scale(coin_img, (35, 35))
		start_x = self.width - life.get_width() - 5

		self.win.blit(text, (start_x - text.get_width() - 10, 65))
		self.win.blit(money, (start_x + 5, 60))

		pygame.display.update()

	def gen_enemies(self):
		"""
		generate the next enemy or enemies to show
		:return: enemy
		"""
		if sum(self.current_wave) == 0:
			self.wave += 1
			self.current_wave = waves[self.wave]
			self.pause = True
		else:
			wave_enemies = [Scorpion(), Wizard(), Club()]
			for x in range(len(self.current_wave)):
				if self.current_wave[x] != 0:
					self.enemies.append(wave_enemies[x])
					self.current_wave[x] = self.current_wave[x] - 1
					break

	def add_tower(self, name):
		x, y = pygame.mouse.get_pos()
		name_list = ["buy_archer", "buy_archer2", "buy_damage", "buy_range"]
		object_list = [ArcherTowerLong(x, y), ArcherTowerShort(x, y), DamageTower(x, y), RangeTower(x, y)]

		try:
			obj = object_list[name_list.index(name)]
			self.moving_object = obj
			obj.moving = True
		except Exception as e:
			print(str(e) + "NOT VALID NAME!")


g = Game()
g.run()
