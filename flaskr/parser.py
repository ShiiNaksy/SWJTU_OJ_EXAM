from flask_restful import reqparse

# Authentication parsers
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str)
login_parser.add_argument('password', type=str)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str)
register_parser.add_argument('password', type=str)
register_parser.add_argument('student_id', type=str)


# Admin parsers
user_query_parser = reqparse.RequestParser()
user_query_parser.add_argument('u_id', type=int)
user_query_parser.add_argument('username', type=str)
user_query_parser.add_argument('student_id', type=int)

## admin login parser
admin_login_parser = reqparse.RequestParser()
admin_login_parser.add_argument('admin_name', type=str)
admin_login_parser.add_argument('password', type=int)

#Exam Charge parsers 
## Exam charge parser - post
exam_charge_parser = reqparse.RequestParser()
exam_charge_parser.add_argument('start_time', type=str)
exam_charge_parser.add_argument('title', type=str)
exam_charge_parser.add_argument('desc', type=str)
exam_charge_parser.add_argument('duration', type=str)
exam_charge_parser.add_argument('problem_set_config', type=str)

## Exam charge parser - get
exam_charge_parser_get = reqparse.RequestParser()
exam_charge_parser_get.add_argument('exam_id', type=int)

## Exam charge parser - delete
exam_charge_parser_delete = reqparse.RequestParser()
exam_charge_parser_delete.add_argument('exam_id', type=int)

## Exam charge parser - put
exam_charge_parser_put = reqparse.RequestParser()
exam_charge_parser_put.add_argument('exam_id', type=int)
### need detailed config of exam format can be seen at doc
exam_charge_parser_put.add_argument('question_set_config', type=str)

## Exams charge - delete
exams_charge_delete = reqparse.RequestParser()
exams_charge_delete.add_argument('exam_ids', type=str)

#Exam parsers
## -get
exam_parser = reqparse.RequestParser()
exam_parser.add_argument('exam_id', type=int) 

#Question parser
## -get
question_parser = reqparse.RequestParser()
question_parser.add_argument('question_id', type=int)

#Questions parser
questions_parser = reqparse.RequestParser()
questions_parser.add_argument('question_ids', type=str)

# Exam parsers
exam_upload_parser = reqparse.RequestParser()
exam_upload_parser.add_argument('student_id', type=int)
exam_upload_parser.add_argument('exam_id', type=int)
exam_upload_parser.add_argument('answers', type=str)

# Judge parsers
judge_parser = reqparse.RequestParser()
judge_parser.add_argument('judgement_id', type=int)
judge_parser.add_argument('q_id', type=int)
judge_parser.add_argument('judged', type=int)
judge_parser.add_argument('right', type=int)
judge_parser.add_argument('score', type=int)
