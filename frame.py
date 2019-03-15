import pymunk

class Frame:

	def __init__(self, space):
		self.space = space

	def addFrame(self):

		#body
		self.bodyBody = pymunk.Body(1, 1666)
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
		headToBodyJoint = pymunk.SlideJoint(self.bodyBody, self.headBody, (0,50), (0,-15),2,3)
		#upper leg connects to body on bottom
		upperLegToBodyJoint = pymunk.SlideJoint(self.bodyBody, self.upperLegsBody, (0,-50) , (0,25) ,2,3)
		#upper leg to lower leg
		upperLegToLowerLegJoint = pymunk.SlideJoint(self.upperLegsBody, self.lowerLegsBody, (0,-25) , (0,25), 2,3)


		self.space.add(self.bodyBody, self.headBody, self.upperLegsBody, self.lowerLegsBody, self.bodyPoly, self.headPoly, self.upperLegsPoly, self.lowerLegsPoly,  headToBodyJoint, upperLegToBodyJoint, upperLegToLowerLegJoint)