import pymunk

class Frame:

	def __init__(self, space):
		self.space = space

	def addFrame(self):

		#body
		self.bodyBody = pymunk.Body(1, 1666)
		self.bodyBody.position = (512,500)
		self.bodyPoly = pymunk.Poly.create_box(self.bodyBody, size=(50,100))

		#head
		self.headBody = pymunk.Body(1, 1666)
		self.headBody.position = (517,530)
		self.headPoly = pymunk.Poly.create_box(self.headBody, size=(30,30))
		
		#Legs
		self.upperLegsBody = pymunk.Body(1, 1666)
		self.upperLegsBody.position = (517,450)
		self.upperLegsPoly = pymunk.Poly.create_box(self.upperLegsBody, size=(30,50))

		self.loweLegsBody = pymunk.Body(1, 1666)
		self.loweLegsBody.position = (517,400)
		self.lowerLegsPoly = pymunk.Poly.create_box(self.loweLegsBody, size=(30,50))

		#arms





		self.space.add(self.bodyBody, self.bodyPoly)
		self.space.add(self.headBody, self.headPoly)
		self.space.add(self.upperLegsBody, self.upperLegsPoly)
		self.space.add(self.loweLegsBody, self.lowerLegsPoly)
