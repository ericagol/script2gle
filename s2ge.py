class S2GSyntaxError(Exception):
	def __init__(self,line,message=''):
		self.line = line
		self.message = message
	def __str__(self):
		return self.line, self.message