import flaskr.db as db
import queue
#TODO: add a sessionmaker here

class Judger:
	def __init__(self, autoJudger):
		self.examResultQ = queue.Queue()	
		self.autoJudger = autoJudger
		# The current should contains a exam score result
		self.current = {}

	def _initCurrent(self):
		pass

	def pushOneExamResult(self):
		pass
	
	def checkNoCoding(self, answer, suppose):
		return answer == suppose
	
	def checkCoding(self, answer, suppose):
		pass		

	def retreiveExamResult(self):
		pass
