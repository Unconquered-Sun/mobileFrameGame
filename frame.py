from PIL import Image
import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math
import os
import csv

class FrameStatistics:
	def __init__(self,headID, bodyID, lArmID, rArmID, legID):
		self.headID = headID
		self.bodyID = bodyID
		self.lArmID = lArmID
		self.rArmID = rArmID
		self.legID = legID
		# self.sprite = 
		self.generateImage()
		print(self.getSize())

	def generateImage(self):
		headImg = Image.open("imgs/head/"+str(self.headID)+".png")
		bodyImg = Image.open("imgs/body/"+str(self.bodyID)+".png")
		legImg = Image.open("imgs/leg/"+str(self.legID)+".png")

		#get anchor points
		
		base_dir = os.path.split(os.path.abspath(__file__))[0]
		
		headAnchors = ()
		bodyToHeadAnchors = ()
		bodyToArmAnchors = ()
		bodyToLegAnchors = ()
		legAnchors = ()

		#head anchor
		headPath = os.path.join(base_dir, "imgs/head/headAnchors.csv")
		with open(headPath) as headCSV:
			headReader = csv.reader(headCSV)
			for row in headReader:
				if str(self.headID) == row[0]:
					headAnchors = (int(row[1].split("/")[0]), int(row[1].split("/")[1]))
					break

		#body to head, leg, and arm anchors
		bodyPath = os.path.join(base_dir, "imgs/body/bodyAnchors.csv")
		with open(bodyPath) as bodyCSV:
			bodyReader = csv.reader(bodyCSV)
			for row in bodyReader:
				if str(self.bodyID) == row[0]:
					bodyToHeadAnchors = (int(row[1].split("/")[0]), int(row[1].split("/")[1]))
					bodyToLegAnchors = (int(row[2].split("/")[0]), int(row[2].split("/")[1]))
					bodyToArmAnchors = (int(row[3].split("/")[0]), int(row[3].split("/")[1]))
					break

		#leg anchor
		legPath = os.path.join(base_dir, "imgs/leg/legAnchors.csv")
		with open(legPath) as legCSV:
			legReader = csv.reader(legCSV)
			for row in legReader:
				if str(self.legID) == row[0]:
					legAnchors = (int(row[1].split("/")[0]), int(row[1].split("/")[1]))

		print(headAnchors, bodyToHeadAnchors, bodyToArmAnchors, bodyToLegAnchors, legAnchors)

		#determine height and width of sprite
		left_of_center = max( [ headAnchors[0], bodyToHeadAnchors[0], legAnchors[0] ] )
		right_of_center = max( [ headImg.size[0]-headAnchors[0], bodyImg.size[0]-bodyToHeadAnchors[0], legImg.size[0]-legAnchors[0] ] )
		self.width = left_of_center+right_of_center
		self.height = bodyImg.size[1]+headImg.size[1]+legImg.size[1]-legAnchors[1]
		
		#create new image
		frameImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
		#insert body
		frameImage.paste(bodyImg, (left_of_center-bodyToHeadAnchors[0] ,headImg.size[1]))
		#head
		frameImage.paste(headImg, (left_of_center-headAnchors[0] ,0) ,headImg )
		#leg
		frameImage.paste(legImg, (left_of_center-legAnchors[0] , headImg.size[1]+bodyToLegAnchors[1]-legAnchors[1] ), legImg )

		#convert image to pygame surface
		imgMode = frameImage.mode
		imgSize = frameImage.size
		imgData = frameImage.tobytes()

		self.frameSprite = pygame.image.fromstring(imgData, imgSize, imgMode).convert_alpha()

		self.armAnchors = ( left_of_center-bodyToHeadAnchors[0]+bodyToArmAnchors[0], headImg.size[1]+bodyToArmAnchors[1] )

	def getSize(self):
		return (self.width, self.height)

	def getFrameImage(self):
		return self.frameSprite

	def getArmAnchors(self):
		return self.armAnchors


class Frame:
	def __init__(self, space):
		self.frameInfo = FrameStatistics(1,1,1,1,1)
		self.space = space

		self.thrusterStr = 200
		#how fast a frame slows down. Must be between 0 and 1
		self.damping = 0.975
		self.rotationalDamping = 0.9


	def addFrame(self, surface):
		#body
		self.bodyBody = pymunk.Body(10, 1666)
		self.bodyBody.position = pymunk.pygame_util.to_pygame((512,400), surface)
		self.bodyPoly = pymunk.Poly.create_box(self.bodyBody, size=self.frameInfo.getSize())

		

		self.space.add(self.bodyBody, self.bodyPoly)

	def addForwardForce(self):

		angle = self.bodyBody.angle
		print(angle )
		vector = Vec2d(math.cos(angle), math.sin(angle))*self.thrusterStr
		self.bodyBody.apply_force_at_local_point( vector, Vec2d(0,0) )
		return vector

	def addBackForce(self):
		angle = self.bodyBody.angle
		print(angle)
		vector = Vec2d(math.cos(angle), math.sin(angle))*self.thrusterStr*-1
		self.bodyBody.apply_force_at_local_point( vector, Vec2d(0,0) )
		return vector

	def addUpForce(self):
		angle = self.bodyBody.angle
		print(angle)
		vector = Vec2d(math.cos(angle), math.sin(angle))*self.thrusterStr
		self.bodyBody.apply_force_at_local_point( vector.perpendicular(), Vec2d(0,0) )
		return vector.perpendicular()

	def addDownForce(self):
		angle = self.bodyBody.angle
		print(angle)
		vector = Vec2d(math.cos(angle), math.sin(angle))*self.thrusterStr*-1
		self.bodyBody.apply_force_at_local_point( vector.perpendicular(), Vec2d(0,0) )
		return vector.perpendicular()

	def rotateRight(self):
		self.bodyBody.apply_force_at_local_point( Vec2d(0,-50), Vec2d(20,20) )
		self.bodyBody.apply_force_at_local_point( Vec2d(0,50), Vec2d(-20,-20) )

	def rotateLeft(self):
		self.bodyBody.apply_force_at_local_point( Vec2d(0,50), Vec2d(20,20) )
		self.bodyBody.apply_force_at_local_point( Vec2d(0,-50), Vec2d(-20,-20) )

	def applyDamping(self):
		if abs(self.bodyBody.velocity.x)>1 or abs(self.bodyBody.velocity.y)>1:
			self.bodyBody.velocity = self.bodyBody.velocity*self.damping
		self.bodyBody.angular_velocity = self.bodyBody.angular_velocity*self.rotationalDamping

	def draw(self, surface):
		angle = math.degrees(self.bodyBody.angle)
		rotatedBody = pygame.transform.rotate(self.frameInfo.getFrameImage(), angle)
		pos = pymunk.pygame_util.to_pygame(self.bodyBody.position, surface) - Vec2d(rotatedBody.get_size()) / 2
		surface.blit(rotatedBody, pos)
		# #head
		# headAngle = math.degrees(self.headBody.angle)
		# rotatedHead = pygame.transform.rotate(self.headSprite, headAngle)
		# headPos = pymunk.pygame_util.to_pygame(self.headBody.position, surface) - Vec2d(rotatedHead.get_size()) / 2
		# surface.blit(rotatedHead, headPos)

		# #body
		# bodyAngle = math.degrees(self.bodyBody.angle)
		# rotatedBody = pygame.transform.rotate(self.bodySprite, bodyAngle)
		# bodyPos = pymunk.pygame_util.to_pygame(self.bodyBody.position, surface) - Vec2d(rotatedBody.get_size()) / 2
		# surface.blit(rotatedBody, bodyPos)

		# #upperLeg
		# uLegAngle = math.degrees(self.upperLegsBody.angle)
		# rotatedULeg = pygame.transform.rotate(self.upperLegSprite, uLegAngle)
		# uLegPos = pymunk.pygame_util.to_pygame(self.upperLegsBody.position, surface) - Vec2d(rotatedULeg.get_size()) / 2
		# surface.blit(rotatedULeg, uLegPos)

		# #lowerLeg
		# lLegAngle = math.degrees(self.lowerLegsBody.angle)
		# rotatedLLeg = pygame.transform.rotate(self.lowerLegSprite, lLegAngle)
		# lLegPos = pymunk.pygame_util.to_pygame(self.lowerLegsBody.position, surface) - Vec2d(rotatedLLeg.get_size()) / 2
		# surface.blit(rotatedLLeg, lLegPos)
