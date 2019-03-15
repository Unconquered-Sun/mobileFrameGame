import sys
import pygame
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
from frame import Frame


class Game:

	def __init__(self):
		pygame.init()
		self.size = width, height = [1024,567]
		self.black = 0,0,0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)


		self.space = pymunk.Space()
		self.space.gravity = Vec2d(0.0, 0.0)

		testFrame = Frame(self.space)
		testFrame.addFrame()

		self.options = pymunk.pygame_util.DrawOptions(self.screen)
		self.space.debug_draw(self.options)

		while True:
			for event in pygame.event.get():
				print(event.type)
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					sys.exit(0)

			self.screen.fill((0,0,0))

			self.space.debug_draw(self.options)

			self.space.step(1/50.0) #3

			pygame.display.flip()
			self.clock.tick(50)




if __name__ == '__main__':
	game = Game()
