import pygame
import pymunk
import os
from PIL import Image

class Camera:
	def update(self, world, screen, targetRect):
		#check if targetRect is within the world boundries
		if targetRect.left<0:
			difference = targetRect.left*-1
			targetRect.left = targetRect.left + difference
			targetRect.right = targetRect.right + difference
		if targetRect.right>world.get_width():
			difference = targetRect.right - world.get_width()
			targetRect.left = targetRect.left - difference
			targetRect.right = targetRect.right - difference
		if targetRect.top<0:
			difference = targetRect.top*-1
			targetRect.top = targetRect.top + difference
			targetRect.bottom = targetRect.bottom + difference
		if targetRect.bottom>world.get_height():
			difference = targetRect.bottom - world.get_height()
			targetRect.top = targetRect.top - difference
			targetRect.bottom = targetRect.bottom - difference

		#create subsurface to render to screen based on targetRect
		worldOutput = world.subsurface(targetRect)
		#blit the subsurface to the screen
		screen.blit(worldOutput, (0,0)  )


class Map:
	def __init__(self,mapFileName):
		base_dir = os.path.split(os.path.abspath(__file__))[0]
		mapPath = os.path.join(base_dir, "maps/"+mapFileName+".txt")
		mapFile = open(mapPath)
		sizeStr = mapFile.readline()

		self.width, self.height = int(sizeStr.split(",")[0]), int(sizeStr.split(",")[1])

		self.world = pygame.Surface((self.width,self.height))

		#generate background data
		backgroundData = mapFile.readline().replace("\n","")
		self.backgroundImage = Image.new('RGBA', (self.width,self.height), (0,0,0,0) )
		if backgroundData == "space":
			self.backgroundImage


		#Add all objects from mapFile
		for entity in mapFile:
			print(entity)
		