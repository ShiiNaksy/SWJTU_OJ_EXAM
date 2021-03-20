import queue
import json
import socket
import threading
from termcolor import colored
from flask import current_app, Blueprint, session, request, g
from flask_restful import Api, Resource
from .log import Logger
from .parser import judge_parser
from . import db

bp = Blueprint('judger', __name__)
api = Api(bp)
l = Logger(location='JUDGE')

#TODO: add teacher judge
class Judge(Resource):
	'''
		This is for teacher to judge 	
	'''

	def get(self):
		args = judge_parser.parse_args(strict=True)
		judgement_id = args.get('judgement_id')
		s = g.Session()
		try:
			judgement = s.query(db.Judgement).filter(db.Judgement.id == judgement_id).first()
			if judgement is None:
				raise Exception("No such judgement")
			msg = {
				"i_status": 1,
				"err_code": -1,
				"msg": "",
				"deliver": json.dumps(judgement, cls=db.AlchemyEncoder)
			}
		except Exception as e:
			l.error(e)
			msg = {
				"i_status": 0,
				"err_code": 10,
				"msg": "No such judgement."
			}

		return msg
	
	def post(self):
		args = judge_parser.parse_args(strict=True)
		s = g.Session()
		try:
			judgement = db.Judgement(
				id=args['judgement_id'],
				q_id=args['q_id'],
				judged=args['judged'],
				right=args['right'],
				score=args['score']
			)
			s.add(judgement)
			s.commit()
			msg = {
				"i_status": 1,
				"err_code": -1,
				"msg": ""
			}
		except:
			s.rollback()
			msg = {
				"i_status": 0,
				"err_code": 1,
				"msg": "Data of judgement insert err."
			}
		finally:
			s.close()

		return msg


class AutoJudge:
	
	def __init__(self, judgeAddr, judgePort):
		self.location = (judgeAddr, judgePort)

		self.sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.judgeIdQueue = queue.Queue()
		self.tasks = queue.Queue() 
		self.dones = queue.Queue()

		for jId in range(1000):
			self.judgeIdQueue.put(jId)

	def reconnect(self):
		self.sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connect()
		
	def connect(self):
		self.sockClient.connect(self.location)

	def ping(self):
		try:
			self.sockClient.send(b'')
		except:
			print(colored('[INFO]', 'red'), " Ping failed connection maybe closed, reconnecting")
			self.reconnect()
			

	def pushOne(self, answerConf):
		'''
		answerConf = {
			'lang': 'lang',
			'code': '',
			'q_in': 'input',
			'suppose': 'output'
		}
		return: jId -> -1 judge full
		'''
		if not judgeIdQueue.emtpy():
			jId = self.judgeIdQueue.get()
			answerConf['jId'] = jId
		else:
			return -1

		self.tasks.put(answerConf)

		return jId
	
	def getOne(self):
		if self.dones.empty():
			return None

		done = self.dones.get()
		jId = done['jId']
		self.judgeIdQueue.put(jId)

		return done
	
	def run(self):
		self.connect()
		#TODO: start a thread here to ping judge server in case of block

		while True:
			if not self.tasks.empty():
				toSend = json.dumps(self.tasks.get())
				self.sockClient.send(toSend)
			else:
				self.ping()
			
			msg = recv_all(self.sockClient)	
			if msg != b'':
				self.dones.put(json.loads(msg))


	
	def disconnect(self):
		self.sockClient.close()


def recv_all(sock):
	BUFF_SIZE = 4096 # 4 KiB
	data = b''
	while True:
		part = sock.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	
	return data
