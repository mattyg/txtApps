class BadCommand(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class BadCellnumber(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class BadJson(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)
