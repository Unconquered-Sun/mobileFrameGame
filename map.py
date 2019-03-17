import pygame
import pymunk

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