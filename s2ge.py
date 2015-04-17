class S2GSyntaxError(Exception):
	def __init__(self,line):
		self.line = line
	def __str__(self):
		return self.line
