class Metrics:
	def __init__(self, *args, **kwargs):
		self.name = kwargs[name]
		self.value = kwargs[value]
		import time
		self.timestamp = int(time.time()
