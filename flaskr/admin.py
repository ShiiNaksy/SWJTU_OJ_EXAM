import jwt
import json
from flask import Flask, Blueprint, session, g
from flask_restful import Api, Resource
from .parser import user_query_parser, admin_login_parser, exam_charge_parser
from . import db, func
from .log import Logger
from passlib.hash import pbkdf2_sha256

l = Logger(location='ADMIN')

bp = Blueprint("admin", __name__)
api = Api(bp)

default_admin = "root"
default_password = "alongpassword"


class AdminAuth(Resource):
    """
    @api {post} /api/amdin/auth/login Login
    @apiName Login
    @apiGroup Admin

    @apiParam {String} admin name
    @apiParam {String} admin password

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.0
    """

    def post(self):
        if g.get('admin'):
            msg = {
                "i_status": 0,
                "err_code": 5,
                "msg": "Already login."
            }
            return msg

        args = admin_login_parser.parse_args(strict=True)
        adminname = args.get('admin_name') or ""
        password = args.get('password') or ""

        if not (adminname and password):
            msg = {
                "i_status": 0,
                "err_code": 0,
                "msg": "admin username or password not provided when admin"
            }
            return msg

        safe = func.check_spell(adminname) and func.check_spell(password)
        if not safe:
            msg = {
                "i_status": 0,
                "err_code": 7,
                "msg": "password or username not format well when."
            }
            return msg

        # TODO: say auth.py, the same
        else:
            s = g.Session()
            try:
                admin = s.query(db.Admins).filter(db.Admins.admin_name == adminname).one()
                pass_hash = admin.password

                if pbkdf2_sha256.verify(password, pass_hash):
                    msg = {
                        "i_status": 1,
                        "err_code": -1,
                        "msg": ""
                    }

                    session['adminname'] = adminname
                    session['admin_id'] = admin.id
                    session['token'] = func.token_gen(admin.id)

                    g.admin = {
                        "admin_id": admin.id
                    }
                    return msg

                else:
                    msg = {
                        "i_status": 0,
                        "err_code": 4,
                        "msg": "password err."
                    }
                    return msg

            except Exception as e:
                # TODO: add a log here
                l.error(e)

                msg = {
                    "i_status": 0,
                    "err_code": 3,
                    "msg": "query err."
                }
                return msg
            finally:
                s.close()


# Users charge
# Users charge based on User charge
# TODO: use sqlalchemy query delete, add, update, get
class UserCharge(Resource):

    def post(self):
        args = user_query_parser.parse_args(strict=True)
        s = g.Session()
        try:
            userinfo = db.Users(
                id=args['u_id'],
                name=args['username'],
                stu_id=args['student_id']
            )
            s.add(userinfo)
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
                "msg": "Data of user insert err."
            }
        finally:
            s.close()

        return msg

    def delete(self):
        args = user_query_parser.parse_args(strict=True)
        user_id = args.get('u_id')
        s = g.Session()
        try:
            user = s.query(db.Users).filter(db.Users.id == user_id).first()

            if user is None:
                raise Exception("No such user")
            else:
                s.delete(user)
                s.commit()

            msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "",
                "deliver": json.dumps(user, cls=db.AlchemyEncoder)
            }
        except Exception as e:
            l.error(e)
            msg = {
                "i_status": 0,
                "err_code": 10,
                "msg": "No such user in users."
            }

        return msg

    def get(self):
        args = user_query_parser.parse_args(strict=True)
        user_id = args.get('u_id')
        s = g.Session()
        try:
            user = s.query(db.Users).filter(db.Users.id == user_id).first()
            if user is None:
                raise Exception("No such user")
            msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "",
                "deliver": json.dumps(user, cls=db.AlchemyEncoder)
            }
        except Exception as e:
            l.error(e)
            msg = {
                "i_status": 0,
                "err_code": 10,
                "msg": "No such user in users."
            }

        return msg


class UsersCharge(Resource):

    def get(self):
        args = user_query_parser.parse_args(strict=True)
        ids = [int(id) for id in args.get('u_id').split(',')]
        s = g.Session()
        result = []
        try:
            for id in ids:
                user = s.query(db.Users).filter(db.Users.id == id).first()
                result.append(json.dumps(user, cls=db.AlchemyEncoder))

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
                "msg": "No such user in users."
            }

        return msg

    def delete(self):
        args = user_query_parser.parse_args(strict=True)
        ids = [int(id) for id in args.get('u_id').split(',')]
        s = g.Session()
        result = []
        try:
            for id in ids:
                user = s.query(db.Users).filter(db.Users.id == id).first()
                if user is None:
                    result.append(json.dumps(user, cls=db.AlchemyEncoder))
                else:
                    s.delete(user)
                    s.commit();

            msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "No such users.",
                "deliver": result
            }
        except Exception as e:
            l.error(e)
            msg = {
                "i_status": 0,
                "err_code": 10,
                "msg": "No such user in users."
            }

        return msg


# Same with UserCharge
class AdminCharge(Resource):

    def post(self):
        args = admin_login_parser.parse_args(strict=True)
        s = g.Session()
        try:
            admin_info = db.Admins(
                admin_name=args['admin_name'],
                password=args['password']
            )
            s.add(admin_info)
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
                "msg": "Data of admin insert err."
            }
        finally:
            s.close()

        return msg

    def delete(self):
        args = admin_login_parser.parse_args(strict=True)
        admin_name = args.get('admin_name')
        s = g.Session()
        try:
            admin = s.query(db.Admins).filter(db.Admins.admin_name == admin_name).first()

            if admin is None:
                raise Exception("No such admin")
            else:
                s.delete(admin)
                s.commit()

            msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "",
                "deliver": json.dumps(admin, cls=db.AlchemyEncoder)
            }
        except Exception as e:
            l.error(e)
            msg = {
                "i_status": 0,
                "err_code": 10,
                "msg": "No such admin in admins."
            }

        return msg

    def get(self):
        args = admin_login_parser.parse_args(strict=True)
        admin_name = args.get('admin_name')
        s = g.Session()
        try:
            admin = s.query(db.Admins).filter(db.Admins.admin_name == admin_name).first()
            if admin is None:
                raise Exception("No such admin")
            msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "",
                "deliver": json.dumps(admin, cls=db.AlchemyEncoder)
            }
        except Exception as e:
            l.error(e)
            msg = {
                "i_status": 0,
                "err_code": 10,
                "msg": "No such admin in admins."
            }

        return msg


# Event receive when user flashing
class EventCharge(Resource):

    def post(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass


# Some infomation must be set for exam
# The configure can be format -json or -yaml
# - exam start time
# - exam duration
# - point weight/percentage of each problem
# a Example format
# config_example = {
#        'title': 'aTitle',
#        'start_time': "a string with time format contains %Y/%m/%d %H:%M:%S",
#        'duration': "%H:%M:%S",
#        # the problem setting must be format like this and convert it to string
#        'problem_set_config': [
#            {
#                'type': 'select',
#                'number': 20,
#                'percentage_tatol': 0.4
#                },
#            {
#                'type': 'fill',
#                'number': 10,
#                'percentage_tatol': 0.2
#                },
#            {
#                'type': 'fix',
#                'number': 10,
#                'percentage_tatol': 0.2
#                },
#            {
#                'type': 'coding',
#                'number': 2,
#                'percentage_tatol': 0.2
#                },
#            ]
#        }
# Need request test
class ExamCharge(Resource):

    def post(self):
        args = exam_charge_parser.parse_args(strict=True)
        err = False
        try:
            config = {
                'start_time': args.get('start_time'),
                'duration': args.get('duration'),
                'problem_set_config': json.dumps(args.get('problem_set_config'))
            }
            exam_configure = func.question_set_config_gen(config)
        except Exception as e:
            l.error(str(e))
            err = True

        if err:
            msg = {
                "i_status": 0,
                "err_code": 8,
                "msg": "Configure format err."
            }
            return msg

        try:
            s = g.Session()
            exam = db.Exams(
                name=args.get('title'),
                start_t=exam_configure.get('start_time'),
                end_t=exam_configure.get('end_time'),
                info=exam_configure.get('info'),
                describe=args.get('desc')
            )
        except Exception as e:
            err = True
            l.error(e)
        finally:
            s.close()

        if err:
            msg = {
                "i_status": 0,
                "err_code": 999,
                "msg": "General Error, no idea how would it happend."
            }
            return msg

        msg = {
            "i_status": 1,
            "err_code": -1,
            "msg": ""
        }
        return msg

    def get(self):
        pass

    def delete(self):
        pass

    # configuration change
    def put(self):
        pass


class ExamsCharge(Resource):

    def get(self):
        pass

    def delete(self):
        pass
