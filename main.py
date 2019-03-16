import sys
import pygame
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
from frame import Frame


class Game:

	def __init__(self):
		self.world = pygame.Surface((10000,10000))
		pygame.init()
		self.size = width, height = [1024,567]
		self.black = 0,0,0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)


		self.space = pymunk.Space()
		self.space.gravity = Vec2d(0.0, 0.0)

		testFrame = Frame(self.space)
		testFrame.addFrame()
		testFrame.addForwardForce()

		self.options = pymunk.pygame_util.DrawOptions(self.screen)
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

			self.screen.fill((0,0,0))
			self.space.debug_draw(self.options)

			output = Vec2d()

			if moveForward == True:
				output = testFrame.addForwardForce()
				pos = testFrame.bodyBody.position
				start = [pos.x,pos.y]
				end = [pos.x+output.x,pos.y-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [start,end], 1)

			if moveBack == True:
				output = testFrame.addBackForce()
				pos = testFrame.bodyBody.position
				start = [pos.x,pos.y]
				end = [pos.x+output.x,pos.y-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [start,end], 1)
			
			if moveUp == True:
				output = testFrame.addUpForce()
				pos = testFrame.bodyBody.position
				start = [pos.x,pos.y]
				end = [pos.x+output.x,pos.y-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [start,end], 1)
			
			if moveDown == True:
				output = testFrame.addDownForce()
				pos = testFrame.bodyBody.position
				start = [pos.x,pos.y]
				end = [pos.x+output.x,pos.y-output.y]
				pygame.draw.lines(self.screen, [255,255,255], False, [start,end], 1)
			
			if rotateRight == True:
				testFrame.rotateRight()

			if rotateLeft == True:
				testFrame.rotateLeft()

			#If not actively moving begin slowing down
			if not( moveForward or moveBack or moveUp or moveDown or rotateLeft or rotateRight ):
				testFrame.applyDamping()


			self.space.step(1/50.0) #3

			pygame.display.flip()
			self.clock.tick(50)




if __name__ == '__main__':
	game = Game()
