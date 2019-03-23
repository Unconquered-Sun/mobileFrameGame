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
	def __init__(self,mapFileName, space):
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
				self.borderWidth = int(child.attrib['x'])
				self.borderHeight = int(child.attrib['y'])
				#create 4 static objects on the borders
				self.topBody = pymunk.Body(body_type=pymunk.Body.STATIC)
				self.topShape = pymunk.Segment(self.topBody, pymunk.pygame_util.to_pygame((0,0),self.world), pymunk.pygame_util.to_pygame((self.borderWidth,0),self.world), 1)
				self.topShape.friction = 1.0 

				self.leftBody = pymunk.Body(body_type=pymunk.Body.STATIC)
				self.leftShape = pymunk.Segment(self.leftBody, pymunk.pygame_util.to_pygame((0,0),self.world), pymunk.pygame_util.to_pygame((0,self.borderHeight),self.world),1)
				self.leftShape.friction = 1.0
				
				self.bottomBody = pymunk.Body(body_type=pymunk.Body.STATIC)
				self.bottomShape = pymunk.Segment(self.bottomBody, pymunk.pygame_util.to_pygame((0,self.borderHeight),self.world), pymunk.pygame_util.to_pygame((self.borderWidth,self.borderHeight),self.world), 1)
				self.bottomShape.friction = 1.0

				self.rightBody = pymunk.Body(body_type=pymunk.Body.STATIC)
				self.rightShape = pymunk.Segment(self.rightBody, pymunk.pygame_util.to_pygame((self.borderWidth,0),self.world), pymunk.pygame_util.to_pygame((self.borderWidth,self.borderHeight),self.world), 1)
				self.rightShape.friction = 1.0

				space.add(self.topBody, self.topShape, self.leftBody, self.leftShape, self.bottomBody, self.bottomShape, self.rightBody, self.rightShape)

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


	def updateBackground(self,surface):
		surface.blit(self.backgroundImage,(0,0))
		