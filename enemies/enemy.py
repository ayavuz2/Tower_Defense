import pygame
import math


path = [(27, 172), (91, 171), (155, 170), (218, 170), (263, 172), (290, 201),
 (348, 203), (411, 203), (475, 202), (539, 203), (604, 203), (668, 203), (731, 203),
  (794, 203), (858, 204), (893, 172), (922, 140), (956, 108), (1019, 108), (1083, 107),
   (1115, 140), (1147, 173), (1165, 189), (1165, 251), (1165, 317), (1165, 358), (1135, 372),
    (1095, 395), (1062, 428), (1007, 428), (940, 428), (875, 428), (810, 428), (746, 428),
     (681, 428), (615, 428), (553, 428), (488, 428), (424, 428), (374, 428), (355, 396), (308, 396), (294, 364),
      (231, 364), (181, 364), (168, 396), (140, 396), (140, 460), (140, 524), (140, 587), (204, 588), (268, 588),
       (333, 588), (398, 588), (461, 588), (525, 588), (550, 588), (562, 620), (585, 620), (594, 650), (654, 650),
        (713, 650), (743, 650), (765, 620), (788, 588), (844, 588), (908, 588), (967, 588), (975, 620), (1036, 620),
         (1097, 620), (1162, 620), (1226, 620), (1293, 620), (1360, 620)]


class Enemy:
	imgs = []

	def __init__(self):
		self.width = 64
		self.height = 64
		self.animation_count = 0
		self.health = 1
		self.max_health = 0
		# self.vel = 3
		self.path = path
		self.x = self.path[0][0]
		self.y = self.path[0][1]
		self.path_pos = 0
		# self.dis = 0
		self.move_count = 0
		self.moved_dis = 0
		self.imgs = []
		self.img = None
		self.left = False
		self.check = False

	def draw(self, win):
		"""
		Draws the enemy with the given images
		:param win: surface
		:return: None
		"""
		self.img = self.imgs[self.animation_count]

		win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
		self.draw_health_bar(win)

	def draw_health_bar(self, win):
		"""
		draw health bar above enemy
		:param win: surface
		:return: None
		"""
		length = 40
		move_by = round(length) / self.max_health
		health_bar = move_by * self.health

		adjust = 15 if self.left else 0
		pygame.draw.rect(win, (255,0,0), (self.x+adjust-30, self.y-40, length, 10), 0)
		pygame.draw.rect(win, (0,255,0), (self.x+adjust-30, self.y-40, health_bar, 10), 0)
		
	def collide(self, X, Y):
		"""
		Returns if position has hit enemy
		:param x: int
		:param y: int
		:return: Bool
		"""
		if X <= self.x + self.width and X >= self.x:
			if Y <= self.y + self.height and Y >= self.y:
				return True
		return False

	def move(self):
		"""
		Move enemy
		:return: None
		"""
		self.animation_count += 1

		if self.animation_count >= len(self.imgs):
			self.animation_count = 0
			
		x1, y1 = self.path[self.path_pos]
		x2, y2 = self.path[self.path_pos+1]		

		move_dis = math.sqrt((x2-x1)**2 + (y2-y1)**2)

		dirn = (x2-x1, y2-y1)
		length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
		dirn = ((dirn[0])/length, (dirn[1])/length)

		# checking to see if flipping is needed or not
		if self.check:
			if dirn[0] < 0: # Moving left
				if not self.left:
					self.flip_imgs()
				self.left = True
				self.check = False
			elif dirn[0] > 0: # Moving right
				if self.left:
					self.flip_imgs()
				self.left = False
				self.check = False

		move_x, move_y = (self.x + dirn[0]*3, self.y + dirn[1]*3) # multiply dirn with int make enemies go faster!
		# self.moved_dis += length

		self.x = move_x
		self.y = move_y

		# Go to next point 				# Looking complex but actually not really
		if dirn[0] > 0: # moving right
			if dirn[1] == 0: # moving right only
				if self.x >= x2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
			elif dirn[1] > 0: # moving down
				if self.x >= x2 and self.y >= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
			else: # moving up
				if self.x >= x2 and self.y <= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])

		elif dirn[0] < 0: # moving left
			if dirn[1] == 0: # moving left only
				if self.x <= x2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
			elif dirn[1] > 0: # moving down
				if self.x <= x2 and self.y >= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
			else: # moving up 
				if self.x <= x2 and self.y <= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
		
		else: # dirn[0] == 0 which means moving up or down only
			if dirn[1] > 0: # moving down
				if self.y >= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])
			else: # moving up
				if self.y <= y2:
					self.path_pos += 1
					self.check = True
					print(self.path[self.path_pos+1])

	def flip_imgs(self):
		for x, img in enumerate(self.imgs):
			self.imgs[x] = pygame.transform.flip(img, True, False)

	def hit(self, damage):
		"""
		Returns if an enemy has died and removes one health for each call
		:return: None
		"""
		self.health -= damage
		if self.health <= 0:
			return True
		return False
