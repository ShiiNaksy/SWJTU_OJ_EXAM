import datetime
import jwt
from flask import current_app, g
from flask.cli import with_appcontext
from . import db 
from .log import Logger
from sqlalchemy import func
import json

l = Logger(location='FUNC')

illegal_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']


def check_spell(username, password):
	"""check_spell.

	:param username:
	:param password:
	"""
	for c in username:
		if c in illegal_characters:
			return False

	for c in password:
		if c in illegal_characters:
			return False

	return True

def check_spell(auth_string):
	for c in auth_string:
		if c in illegal_characters:
			return False

	return True

def escape(string):
	#TODO: adding safe 
	return string

def token_retrieve(token):
	return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

def token_gen(user_id):
	payload = {
			"exp": datetime.datetime.now() + datetime.timedelta(days=7),
			"iat": datetime.datetime.now(),
			"sub": user_id
			}
	token = jwt.encode(
		payload,
		current_app.config['SECRET_KEY'],
		algorithm='HS256'
		)

	return token

## Example of config
# config = {
#		 'start_time': '2021/03/02 09:57:00',
#		 'duration': '02:00:00',
#		 'problem_set_config': [
#			 {
#				 'type': 'select',
#				 'number': 20,
#				 'percentage_tatol': 0.4
#				 },
#			 {
#				 'type': 'fill',
#				 'number': 10,
#				 'percentage_tatol': 0.2
#				 },
#			 {
#				 'type': 'fix',
#				 'number': 10,
#				 'percentage_tatol': 0.2
#				 },
#			 {
#				 'type': 'coding',
#				 'number': 2,
#				 'percentage_tatol': 0.2
#				 },
#			 ]
#	 }
## A sample of output
# {'start_time': datetime.datetime(2021, 3, 2, 9, 57), 'end_time': datetime.datetime(2021, 3, 2, 11, 57), 'question_set': {'select': [56, 30, 68, 67, 52, 28, 12, 69, 81, 87, 83, 84, 16, 63, 14, 90, 88, 33, 99, 92], 'fill': [330, 323, 383, 340, 365, 318, 367, 322, 310, 363], 'fix': [264, 229, 209, 245, 263, 299, 233, 275, 262, 250], 'coding': [129, 132]}, 'score_config': [{'type': 'select', 'percentage': 0.4}, {'type': 'fill', 'percentage': 0.2}, {'type': 'fix', 'percentage': 0.2}, {'type': 'coding', 'percentage': 0.2}]}
def question_set_config_gen(config):
	# TODO: need seperate the time parse
	start_time_str = config.get('start_time') 
	duration_str = config.get('duration') 
	question_set_config = config.get('problem_set_config') 

	# time caculate
	start_time = datetime.datetime.strptime(start_time_str, '%Y/%m/%d %H:%M:%S')
	duration = datetime.datetime.strptime(duration_str, '%H:%M:%S')
	duration = datetime.timedelta(
		hours= duration.hour,
		minutes= duration.minute,
		seconds= duration.second
	)

	end_time = start_time + duration

	# problem set gen
	score_config = []
	problem_set = {
		'select': [],
		'fill': [],
		'fix': [],
		'coding': []
	} 

	s = g.Session()
	try:
		for p_conf in question_set_config:
			t = p_conf.get('type')
			count = p_conf.get('number')
			l.debug("CONF:" + str(p_conf))
			if count < 0:
				l.error('the configure setting is format err.')
				raise Exception
			score_per = p_conf.get('percentage_tatol')
			score_config.append(
				{'type': t, 'percentage': score_per}
			)
			q = s.query(db.Questions).filter(db.Questions.question_type == t)
			db_count = q.count()
			if count > db_count:
				l.error('the number of ' + t + 'problem set is not enough' + 'current ' + db_count + 'need ' + count + '.')
				raise Exception
				
			problems = q.order_by(func.rand()).limit(count).all()
			for problem in problems:
				problem_set[t].append(problem.id)

	except Exception as e:
		l.error(e)
	finally:
		s.close()

	configure = {
		'start_time': start_time,
		'end_time': end_time,
		'question_set': problem_set,
		'score_config': score_config
	}

	return configure

	
	


#config = {
#	"start_time": "2021/03/02 09:57:00",
#	"duration": "02:00:00",
#	"problem_set_config": [
#		{
#			"type": "select",
#			"number": 20,
#			"percentage_tatol": 0.4
#			},
#		{
#			"type": "fill",
#			"number": 10,
#			"percentage_tatol": 0.2
#			},
#		{
#			"type": "fix",
#			"number": 10,
#			"percentage_tatol": 0.2
#			},
#		{
#			"type": "coding",
#			"number": 2,
#			"percentage_tatol": 0.2
#			},
#		]
#}
#print( question_set_config_gen(config) )
#
