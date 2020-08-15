import pygame
import os
from .enemy import Enemy


class Scorpion(Enemy):
	imgs = []

	for x in range(20):
		add_str = str(x)
		if x < 10:
			add_str = "0" + add_str
		imgs.append(pygame.image.load(os.path.join("game_assets/enemies/1", "1_enemies_1_run_0" + add_str + ".png")))

	def __init__(self):
		super().__init__()