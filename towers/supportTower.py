import pygame
import os
import math
import time
from .tower import Tower


class RangeTower(Tower):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.radius = 150

	def draw(self, win):
		super().draw_radius(win)
		super().draw(win)