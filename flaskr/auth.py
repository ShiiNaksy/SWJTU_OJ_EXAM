import jwt
import datetime
from flask import current_app, Blueprint, session, request, g
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256
from . import db, func
from . import parser
from .log import Logger

bp = Blueprint('auth', __name__)
api = Api(bp)
l = Logger(location='{AUTH}')

@bp.before_app_request
def load_lobbed_in_user():
    token = session.get('token')
    if  not token:
        l.info("session has no token")
        return 


    l.info(token) 
    try:
        payload = func.token_retrieve(token)
        l.info(str(payload))
        g.user  = {
                "user_id":  payload['sub'],
                }
        print("Finish before request")
    except jwt.exceptions.ExpiredSignatureError:
        l.warn("token expired.")
        g.user = None
        pass
    except Exception as e:
#        l.error("load user session error." + str(e))
        g.user = None
    

class Register(Resource):
    """Register."""

    """
    @api {post} /api/auth/register Register
    @apiName Register
    @apiGroup Auth

    @apiParam {String} username User's name. 
    @apiParam {String} password Password.
    @apiParam {int} student_id User's student id. 

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def post(self):
        args = parser.register_parser.parse_args(strict=True)
        username = args.get('username')
        password = args.get('password')
        student_id = args.get('student_id')
        
        if not (username and password and student_id):
            msg = {
                    "i_status": 0,
                    "err_code": 2,
                    "msg": "username or password or student_id not provided"
                    }
            return msg


        safe = func.check_spell(username) and func.check_spell(password)
        if not safe:
            msg = {
                    "i_status": 0,
                    "err_code": 0,
                    "msg": "username or password err."
                    }
        else:
            s = g.Session()
            try:
                user = db.Users(
                        name=username, 
                        password=pbkdf2_sha256.hash(password),
                        stu_id=student_id
                        )
                s.add(user)
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

class Login(Resource):
    """
    @api {post} /api/auth/login Login
    @apiName Login
    @apiGroup Auth

    @apiParam {String} username User's name. 
    @apiParam {String} password Password.

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def post(self):
        if g.get('user'):
            msg = {
                    "i_status": 0,
                    "err_code": 5,
                    "msg": "Already login."
                    }
            pass
            
        args = parser.login_parser.parse_args(strict=True)
        username = args.get("username") 
        password = args.get("password") 

        if not (username and password):
            msg = {
                    "i_status": 0,
                    "err_code": 2,
                    "msg": "username or password not provided"
                    }
            return msg

        safe = func.check_spell(username) and func.check_spell(password)

        if safe:
            s = g.Session()
            try:
                user = s.query(db.Users).filter(db.Users.name == username).one()
                pass_hash = user.password

                if pbkdf2_sha256.verify(password, pass_hash):
                    msg = {
                            "i_status": 1,
                            "err_code": -1,
                            "msg": ""
                            }
        
                    session['username'] = username
                    session['user_id'] = user.id
                    session['token'] = func.token_gen(user.id)

                    g.user = {
                            "user_id": user.id
                            }

                else:
                    msg = {
                            "i_status": 0,
                            "err_code": 4,
                            "msg": "password err."
                            }
            except Exception as e:
                l.error(e)

                msg = {
                        "i_status": 0,
                        "err_code": 3,
                        "msg": "query err."
                        }
            finally:
                s.close()

        return msg

class Logout(Resource):
    """
    @api {get} /api/auth/logout Logout
    @apiName Logout
    @apiGroup Auth

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def get(self):
        session.clear()
        g.user = None
        msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": ""
                }
        
        return msg



api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
