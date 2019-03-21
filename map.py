import pygame
import pymunk
import os
from PIL import Image, ImageDraw
import random

class Camera:
	def update(self, world, screen, targetRect):
		#check if targetRect is within the world boundries
		if targetRect.left<0:
			print("ping 1")
			targetRect.left = 0
			targetRect.right = screen.get_width()
			print(targetRect)
		# if targetRect.right>world.get_width():

		# 	print(targetRect.right,world.get_width())
		# 	print("ping 2")
		# 	difference = targetRect.right - world.get_width()
		# 	targetRect.left = targetRect.left - difference
		# 	targetRect.right = targetRect.right - difference

		# 	print(targetRect)
		# if targetRect.top<0:
		# 	print("ping 3")
		# 	difference = targetRect.top*-1
		# 	targetRect.top = targetRect.top + difference
		# 	targetRect.bottom = targetRect.bottom + difference
		# if targetRect.bottom>world.get_height():
		# 	print("ping 4")
		# 	difference = targetRect.bottom - world.get_height()
		# 	targetRect.top = targetRect.top - difference
		# 	targetRect.bottom = targetRect.bottom - difference

		#create subsurface to render to screen based on targetRect
		print(targetRect)
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
		backgroundImage = Image.new('RGBA', (self.width,self.height), (0,0,0,0) )
		if backgroundData == "space":
			backgroundImage.paste( (0,0,0,255), [0,0,backgroundImage.size[0],backgroundImage.size[1]] )
			drawImage = ImageDraw.Draw(backgroundImage)
			for x in range(self.width*2):
				randX = random.randint(0,self.width)
				randY = random.randint(0,self.height)
				radius = random.randint(1,5)
				color = ( random.randint(150,255),random.randint(150,255),random.randint(150,255),255 )
				drawImage.ellipse([ (randX, randY), (randX+radius,randY+radius) ], color,color)
		
		imgMode = backgroundImage.mode
		print(imgMode)
		imgSize = backgroundImage.size
		imgData = backgroundImage.tobytes()	

		self.backgroundImage = pygame.image.fromstring(imgData, imgSize, imgMode).convert_alpha()

		#Add all objects from mapFile
		for entity in mapFile:
			print(entity)

	def updateBackground(self,surface):
		surface.blit(self.backgroundImage,(0,0))
		