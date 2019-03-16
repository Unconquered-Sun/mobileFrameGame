import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math

class Frame:

	def __init__(self, space):
		self.space = space

		self.thrusterStr = 200
		#how fast a frame slows down. Must be between 0 and 1
		self.damping = 0.975
		self.rotationalDamping = 0.9

		self.bodySprite = pygame.image.load("imgs/body/01.jpg").convert_alpha()
		self.headSprite = pygame.image.load("imgs/heads/01.jpg").convert_alpha()
		# self.upperLegSprite
		# self.lowerLegSprite

	def addFrame(self):
		#body
		self.bodyBody = pymunk.Body(10, 1666)
		self.bodyBody.position = (512,400)
		self.bodyPoly = pymunk.Poly.create_box(self.bodyBody, size=(50,100))

		#head
		self.headBody = pymunk.Body(1, 1666)
		self.headBody.position = (517,470)
		self.headPoly = pymunk.Poly.create_box(self.headBody, size=(30,30))
		

		#Legs
		self.upperLegsBody = pymunk.Body(1, 1666)
		self.upperLegsBody.position = (517,350)
		self.upperLegsPoly = pymunk.Poly.create_box(self.upperLegsBody, size=(30,50))

		self.lowerLegsBody = pymunk.Body(1, 1666)
		self.lowerLegsBody.position = (517,300)
		self.lowerLegsPoly = pymunk.Poly.create_box(self.lowerLegsBody, size=(30,50))

		#arms

		#joints
		#head connects to body on top
		headToBodyJoint = pymunk.SlideJoint(self.bodyBody, self.headBody, (0,50), (0,-15),0,1)
		
		#upper leg connects to body on bottom
		upperLegToBodyJoint = pymunk.SlideJoint(self.bodyBody, self.upperLegsBody, (0,-50) , (0,25) ,2,3)
		
		#upper leg to lower leg knee joints
		upperLegToLowerLegJoint1 = pymunk.SlideJoint(self.upperLegsBody, self.lowerLegsBody, (-15,-25) , (-15,25), 2,3)
		upperLegToLowerLegJoint2 = pymunk.SlideJoint(self.upperLegsBody, self.lowerLegsBody, (15,-25) , (15,25), 0,20)

		self.space.add(self.bodyBody, self.headBody, self.upperLegsBody, self.lowerLegsBody, self.bodyPoly, self.headPoly, self.upperLegsPoly, self.lowerLegsPoly, headToBodyJoint, upperLegToBodyJoint, upperLegToLowerLegJoint1, upperLegToLowerLegJoint2)

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
		#head
		headAngle = math.degrees(self.headBody.angle)
		rotatedHead = pygame.transform.rotate(self.headSprite, headAngle)
		headPos = pymunk.pygame_util.to_pygame(self.headBody.position, surface) - Vec2d(rotatedHead.get_size()) / 2
		surface.blit(rotatedHead, headPos)

		#body
		bodyAngle = math.degrees(self.bodyBody.angle)
		rotatedBody = pygame.transform.rotate(self.bodySprite, bodyAngle)
		bodyPos = pymunk.pygame_util.to_pygame(self.bodyBody.position, surface) - Vec2d(rotatedBody.get_size()) / 2
		surface.blit(rotatedBody, bodyPos)