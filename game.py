import pygame
import os
import math
import time
import random
from enemies.scorpion import Scorpion
from enemies.wizard import Wizard
from enemies.club import Club
from enemies.enemy import path
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu, PlayPauseButton
pygame.font.init()
pygame.init()


lives_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "heart.png")), (48,48))
coin_img = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "sell.png")), (35, 35))

play_button = pygame.image.load(os.path.join("game_assets", "play.png"))
pause_button = pygame.image.load(os.path.join("game_assets", "pause.png"))

unmute_button = pygame.image.load(os.path.join("game_assets", "unmute.png"))
mute_button = pygame.image.load(os.path.join("game_assets", "mute.png")) 

wave_bg = pygame.transform.scale(
	pygame.image.load(os.path.join("game_assets", "wave.png")), (180, 56))

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

PATH = path

# load music
pygame.mixer.music.load(os.path.join("game_assets", "music1.mp3"))

# waves are in form
# frequency of enemies
# (# scorpion, # wizard, # club)
waves = [
	[10, 0, 0], [20, 0, 0], [30, 0, 0], [40, 0, 0], [30, 10, 0], [20, 20, 0], [10, 30, 0],
	 [10, 40, 0], [20, 40, 0], [30, 30, 5], [0, 40, 10], [0, 30, 20], [10, 20, 30], [0, 0, 40], [40, 40, 40]
]


class Game:
	def __init__(self, win):
		self.width = 1366
		self.height = 768
		self.win = win
		self.enemies = []
		self.attack_towers = []
		self.support_towers = []
		self.lives = 10
		self.money = 2000
		self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
		# self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
		self.timer = time.time()
		self.life_font = pygame.font.SysFont("comicsans", 50)
		self.selected_tower = None
		self.paused = True
		self.music_off = True
		self.wave = 0
		self.current_wave = waves[self.wave][:]
		self.moving_object = None
		self.menu = VerticalMenu(self.width - side_img.get_width() + 30, 140, side_img)
		self.menu.add_button(buy_archer, "buy_archer", 500)
		self.menu.add_button(buy_archer2, "buy_archer2", 700)
		self.menu.add_button(buy_damage, "buy_damage", 1000)
		self.menu.add_button(buy_range, "buy_range", 1000)
		self.playPauseButton = PlayPauseButton(play_button, pause_button, 10, self.height - 85)
		self.musicButton = PlayPauseButton(unmute_button, mute_button, 84, self.height - 85)

	def run(self):
		run = True
		clock = pygame.time.Clock()

		while run:
			clock.tick(30)

			if self.paused == False:
				# gen monsters
				if time.time() - self.timer >= random.randrange(2, 5)/2:
					self.timer = time.time()
					self.gen_enemies()

			pos = pygame.mouse.get_pos()

			# check for moving object
			if self.moving_object:
				self.moving_object.move(pos[0], pos[1])
				collide = False
				tower_list = self.attack_towers[:] + self.support_towers[:]
				for tower in tower_list:
					if tower.collide(self.moving_object):
						collide = True
						tower.place_color = (255,0,0, 100)
						self.moving_object.place_color = (255,0,0, 100)
					else:
						tower.place_color = (0,0,255, 100)
						if not(collide):
							self.moving_object.place_color = (0,0,255, 100)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					# print(pos[0], pos[1])
					# if you are moving an object and click
					if self.moving_object:
						not_allowed = False
						tower_list = self.attack_towers[:] + self.support_towers[:]
						for tower in tower_list:
							if tower.collide(self.moving_object):
								not_allowed = True

						if not not_allowed and self.point_to_line(self.moving_object):
							if self.moving_object.name in attack_tower_names:
								self.attack_towers.append(self.moving_object)

							elif self.moving_object.name in support_tower_names:
								self.support_towers.append(self.moving_object)
							
							self.moving_object.moving = False
							self.moving_object = None
							# print([tower.name for tower in self.attack_towers[:]])
							print("Done")

					else:
						# check for play or pause
						if self.playPauseButton.click(pos[0], pos[1]):
							self.paused = not(self.paused)
							self.playPauseButton.paused = self.paused

						# check for mute or unmute
						if self.musicButton.click(pos[0], pos[1]):
							self.music_off = not(self.music_off)
							self.musicButton.paused = self.music_off
							if self.music_off:
								pygame.mixer.music.pause()
							else:
								pygame.mixer.music.play()
								

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

			if not(self.paused):
				# loop through enemies
				to_del = []
				for en in self.enemies:
					en.move()
					if en.x > 1340:
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

			"""
			for point in PATH:
				pygame.draw.circle(self.win, (255,0,0), (point[0], point[1]), 5)

			pygame.display.update()
			"""

		pygame.quit()

	def draw(self):
		self.win.blit(self.bg, (0,0))

		# draw placement rings
		if self.moving_object:
			for tower in self.attack_towers:
				tower.draw_placement(self.win)

			for tower in self.support_towers:
				tower.draw_placement(self.win)

			self.moving_object.draw_placement(self.win)

		# draw attack towers
		for tw in self.attack_towers:
			tw.draw(self.win)
		
		# draw support towers
		for tw in self.support_towers:
			tw.draw(self.win)

		# draw enemies
		for en in self.enemies:
			en.draw(self.win)

		# redraw selected tower
		if self.selected_tower:
			self.selected_tower.draw(self.win)
		
		# draw moving object
		if self.moving_object:
			self.moving_object.draw(self.win)

		# draw menu
		self.menu.draw(self.win)

		# draw play pause button
		self.playPauseButton.draw(self.win)

		# draw music toggle button
		self.musicButton.draw(self.win)

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

		# draw wave
		self.win.blit(wave_bg, (10, 10))
		text = self.life_font.render("Wave #" + str(self.wave), 1, (255,255,255))
		self.win.blit(text,(10 + wave_bg.get_width()//2 - text.get_width()//2, 20))

		pygame.display.update()

	def point_to_line(self, tower):
		"""
		returns if you can place tower based on distance from path
		:param tower: Tower
		:return: Bool
		"""
		# find two closest points
		closest = []
		for point in PATH:
			dis = math.sqrt((tower.x - point[0])**2 + (tower.y - point[1])**2)
			closest.append([dis, point])

		closest.sort(key=lambda x: x[0])
		closest1 = closest[0][1] # (x1, y1)
		closest2 = closest[1][1] # (x2, y2)

		try:
			slope = (closest2[1] - closest1[1]) / (closest2[0] - closest1[0]) # (y2-y1) / (x2-x1)
			A = slope
			B = -1
			C = closest1[1] - slope*closest1[0]
		except ZeroDivisionError:
			slope = 0
			A = -1
			B = slope
			C = closest1[0] - slope*closest1[1]

		dis = abs(A*tower.x + B*tower.y + C) / math.sqrt(A**2 + B**2)
		# print(dis, closest1, closest2, (tower.x, tower.y))

		return True if dis >= tower.width//2 + 10 else False

	def gen_enemies(self):
		"""
		generate the next enemy or enemies to show
		:return: enemy
		"""
		if sum(self.current_wave) == 0:
			if len(self.enemies) == 0:
				self.wave += 1
				self.current_wave = waves[self.wave]
				self.paused = True
				self.playPauseButton.paused = self.paused
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


win = pygame.display.set_mode((1366, 768))
g = Game(win)
g.run()
