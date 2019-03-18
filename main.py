import sys
import pygame
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
from frame import Frame
from map import Camera, Map


class Game:

	def __init__(self):
		pygame.init()

		self.map = Map("map01")

		self.world = pygame.Surface((6025,4567))
		
		self.size = width, height = [1024,567]
		self.black = 0,0,0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)
		self.camera = Camera()

		self.space = pymunk.Space()
		self.space.gravity = Vec2d(0.0, 0.0)

		testFrame = Frame(self.space)
		testFrame.addFrame(self.world)

		self.options = pymunk.pygame_util.DrawOptions(self.world)
		self.space.debug_draw(self.options)

		moveForward = False
		moveBack = False
		moveUp = False
		moveDown = False
		rotateRight = False
		rotateLeft = False

		while True:
			for event in pygame.event.get():
				# print(event.type)
				# testFrame.addForwardForce()
				if event.type == pygame.QUIT:
					sys.exit(0)
				
				elif event.type == pygame.KEYDOWN:
					print(event.key)
					if event.key == pygame.K_ESCAPE:
						sys.exit(0)
					elif event.key == pygame.K_d:
						moveForward = True
					elif event.key == pygame.K_a:
						moveBack = True
					elif event.key == pygame.K_w:
						moveUp = True
					elif event.key == pygame.K_s:
						moveDown = True
					elif event.key == pygame.K_e:
						rotateRight = True
					elif event.key == pygame.K_q:
						rotateLeft = True

				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_d:
						moveForward = False
					elif event.key == pygame.K_a:
						moveBack = False
					elif event.key == pygame.K_w:
						moveUp = False
					elif event.key == pygame.K_s:
						moveDown = False
					elif event.key == pygame.K_e:
						rotateRight = False
					elif event.key == pygame.K_q:
						rotateLeft = False


			output = Vec2d()

			if moveForward == True:
				output = testFrame.addForwardForce()
				pos = pymunk.pygame_util.to_pygame(testFrame.mainBody.position , self.world)
				end = [pos[0]+output.x,pos[0]-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [pos,end], 1)

			if moveBack == True:
				output = testFrame.addBackForce()
				pos = pymunk.pygame_util.to_pygame(testFrame.mainBody.position , self.world)
				end = [pos[0]+output.x,pos[0]-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [pos,end], 1)
			
			if moveUp == True:
				output = testFrame.addUpForce()
				pos = pymunk.pygame_util.to_pygame(testFrame.mainBody.position , self.world)
				end = [pos[0]+output.x,pos[0]-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [pos,end], 1)
			
			if moveDown == True:
				output = testFrame.addDownForce()
				pos = pymunk.pygame_util.to_pygame(testFrame.mainBody.position , self.world)
				end = [pos[0]+output.x,pos[0]-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [pos,end], 1)
			
			if rotateRight == True:
				testFrame.rotateRight()

			if rotateLeft == True:
				testFrame.rotateLeft()

			#If not actively moving begin slowing down
			if not( moveForward or moveBack or moveUp or moveDown or rotateLeft or rotateRight ):
				testFrame.applyDamping()

			self.world.fill((0,0,0))
			#draw everything in the world
			testFrame.draw(self.world)

			self.camera.update(self.world, self.screen, testFrame.getRect(self.world,self.size))

			# worldOutput = self.world.subsurface(testFrame.getRect(self.world,self.size))
			# self.screen.blit(worldOutput, (0,0)  )

			self.space.step(1/50.0)

			pygame.display.flip()
			self.clock.tick(50)




if __name__ == '__main__':
	game = Game()
