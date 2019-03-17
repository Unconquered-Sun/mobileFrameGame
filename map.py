import pygame
import pymunk

class Camera:
	def __init__(self, width, height):
		self.camera = pygame.Rect(0,0,width, height)
		self.width = width
		self.height = height

