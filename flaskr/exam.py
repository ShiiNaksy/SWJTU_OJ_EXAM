from flask import Flask, Blueprint, session, g
from flask_restful import Api, Resource
from .parser import exam_parser, questions_parser, question_parser, exam_upload_parser
from .log import Logger
from . import db
import json

l = Logger(location="Exam")

bp = Blueprint("exam", __name__)
api = Api(bp)


#The get method is about to return a problem set of a exam
class Exam(Resource):

	def get(self):
		args = exam_parser.parse_args(strict=True)
		exam_id = args.get("exam_id")

		s = g.Session()
		try:
			exam = s.query(db.Exams).filter(db.Exams.id == exam_id).first()
			msg = {
					"i_status": 1,
					"err_code": -1,
					"msg": "",
					"deliver": exam.get("info")
					}
		except Exception as e:
			l.error(e)
			msg = {
					"i_status": 0,
					"err_code": 9,
					"msg": "No such exam."
					}

		return msg
	
	# TODO: upload exam result to server
	"""
	@api {post} /api/exam
	@apiName upload a exam
	@apiGroup Exam

	@apiParam {Number} exam_id Exam id
	@apiParam {Number} student_id User's student id. 
	@apiParam {String} answers Answers

	@apiSuccess {Number} i_status Instruction success status.
	@apiSuccess {Number} err_code Error code.
	@apiSuccess {String} msg Message.
	@apiVersion 0.0.1
	"""
	def post(self):
		'''
		answers format should a list of {'q_id': (int), 'answer': (string)}
		so just need send it to ExamResult
		then wait to be judge
		'''
		args = exam_upload_parser.parse_args(strict=True)
		s = g.Session()
		try:
			examResult = db.ExamResult(
				exam_id = args['exam_id'],
				stu_id = args['student_id'],
				answers = args['answers']
			)
			s.add(examResult)
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
					"msg": "Data insert err."
					}
		finally:
			s.close()

		return msg
			

class Question(Resource):
	
	def get(self):
		args = question_parser.parse_args(strict=True)
		question_id = args.get('question_id')
		s = g.Session()
		try:
			question = s.query(db.Questions).filter(db.Questions.id == question_id).first()
			if question is None:
				raise Exception("No such question")
			msg = {
					"i_status": 1,
					"err_code": -1,
					"msg": "",
					"deliver": json.dumps(question, cls=db.AlchemyEncoder)
					}
		except Exception as e:
			l.error(e)
			msg = {
					"i_status": 0,
					"err_code": 10,
					"msg": "No such question in exam."
					}

		return msg

		

class Questions(Resource):
	
	def get(self):
		args = questions_parser.parse_args(strict=True)
		ids = [ int(id) for id in args.get('question_ids').split(',') ]
		s = g.Session()
		result = [] 
		try:
			for id in ids:
				question = s.query(db.Questions).filter(db.Questions.id == id).first()
				result.append(json.dumps(question, cls=db.AlchemyEncoder))

			msg = {
					"i_status": 1,
					"err_code": -1,
					"msg": "",
					"deliver": result
					}
		except Exception as e:
			l.error(e)
			msg = {
					"i_status": 0,
					"err_code": 10,
					"msg": "No such question in exam."
					}

		return msg

api.add_resource(Exam, '/exam')
api.add_resource(Question, '/question')
api.add_resource(Questions, '/questions')
