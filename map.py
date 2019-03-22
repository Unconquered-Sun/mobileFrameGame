import pygame
import pymunk
import os
from PIL import Image, ImageDraw
import random
import xml.etree.ElementTree as ET

class Camera:
	def update(self, world, screen, targetRect):
		#check if targetRect is within the world boundries
		print(targetRect)
		# print(world.get_width(),world.get_height())

		left = targetRect.left
		right = targetRect.right-left
		top = targetRect.top
		bottom = targetRect.bottom-top

		print(left,top,right,bottom)

		if left<0:
			print("1")
			left = 0
			right = screen.get_width()
		
		if right>(world.get_width()//2):
			print("2")
			left = (world.get_width()//2) - screen.get_width()
			right = (world.get_width()//2)
		
		if top<0:
			print("3")
			top = 0
			bottom = screen.get_height()
		
		if bottom>(world.get_height()//2):
			print("4")
			top = (world.get_height()//2) - screen.get_height()
			bottom = (world.get_height()//2)

		#create subsurface to render to screen based on targetRect
		outputRect = pygame.Rect(left,top,right,bottom)
		# print(left,top,right,bottom)
		print(outputRect)
		worldOutput = world.subsurface(outputRect)
		#blit the subsurface to the screen
		screen.blit(worldOutput, (0,0)  )


class Map:
	def __init__(self,mapFileName):
		# base_dir = os.path.split(os.path.abspath(__file__))[0]
		# mapPath = os.path.join(base_dir, "maps/"+mapFileName+".txt")
		# mapFile = open(mapPath)
		mapFile2 = ET.parse("maps/"+mapFileName+".xml")
		mapRoot = mapFile2.getroot()


		for child in mapRoot:
			if child.tag == "SIZE":
				#Create surface
				self.width = int(child.attrib['x'])
				self.height = int(child.attrib['y'])
				self.world = pygame.Surface( (self.width, self.height) )
			elif child.tag == "BORDER":
				#Create border
				None

			elif child.tag == "TYPE":
				#Create Background Image based on type
				if child.attrib['type'] == "space":
					backgroundImage = Image.new('RGBA', (self.width,self.height), (0,0,0,0) )
					backgroundImage.paste( (0,0,0,255), [0,0,backgroundImage.size[0],backgroundImage.size[1]] )
					drawImage = ImageDraw.Draw(backgroundImage)
					for x in range(self.width*2):
						randX = random.randint(0,self.width)
						randY = random.randint(0,self.height)
						radius = random.randint(1,5)
						color = ( random.randint(150,255),random.randint(150,255),random.randint(150,255),255 )
						drawImage.ellipse([ (randX, randY), (randX+radius,randY+radius) ], color,color)

					imgMode = backgroundImage.mode
					imgSize = backgroundImage.size
					imgData = backgroundImage.tobytes()

					self.backgroundImage = pygame.image.fromstring(imgData, imgSize, imgMode).convert_alpha()

			elif child.tag == "ENTITIES":
				#Populate Map
				None


		# sizeStr = mapFile.readline()

		# self.width, self.height = int(sizeStr.split(",")[0]), int(sizeStr.split(",")[1])
		# # print(self.width, self.height)
		# self.world = pygame.Surface((self.width,self.height))

		# #generate background data
		# backgroundData = mapFile.readline().replace("\n","")
		# backgroundImage = Image.new('RGBA', (self.width,self.height), (0,0,0,0) )
		# if backgroundData == "space":
		# 	backgroundImage.paste( (0,0,0,255), [0,0,backgroundImage.size[0],backgroundImage.size[1]] )
		# 	drawImage = ImageDraw.Draw(backgroundImage)
		# 	for x in range(self.width*2):
		# 		randX = random.randint(0,self.width)
		# 		randY = random.randint(0,self.height)
		# 		radius = random.randint(1,5)
		# 		color = ( random.randint(150,255),random.randint(150,255),random.randint(150,255),255 )
		# 		drawImage.ellipse([ (randX, randY), (randX+radius,randY+radius) ], color,color)
		
		# imgMode = backgroundImage.mode
		# imgSize = backgroundImage.size
		# imgData = backgroundImage.tobytes()	

		# self.backgroundImage = pygame.image.fromstring(imgData, imgSize, imgMode).convert_alpha()

		# #Add all objects from mapFile
		# for entity in mapFile:
		# 	print(entity)

	def updateBackground(self,surface):
		surface.blit(self.backgroundImage,(0,0))
		