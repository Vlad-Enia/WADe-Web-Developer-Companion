from flask import Flask, request, make_response, jsonify, abort
from hashlib import sha256
import pymongo
import yaml
import sys
import os
import datetime
import jwt

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)


os.chdir(r'C:\Users\eniav\Desktop\WADe-Web-Developer-Companion\backend\login')

with open('config.yaml', 'r') as file:
    db_config = yaml.safe_load(file)

try:
    client = pymongo.MongoClient(db_config['db']['db_url'], server_api=pymongo.server_api.ServerApi(db_config['db']['db_server_api']))
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

SECRET_KEY="secret"    

db = client.WDC
user_collection = db['users']


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e
    
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return 'ok', payload['sub']
    except jwt.ExpiredSignatureError:
        return 'err', 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'err', 'Invalid token. Please log in again.'

@app.route("/login", methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
        username = request.args.get('username','')
        password = request.args.get('password','')
        encoded_password = sha256(password.encode('UTF-8')).hexdigest()
        user_db = user_collection.find_one({'username': username})
        if user_db is None or encoded_password != user_db['password']:
            abort(401)
        else:

            try:
                auth_token = encode_auth_token(username)
                if(auth_token):
                    response = jsonify({
                        "access_token": auth_token
                    })
                    _corsify_actual_response(response)
                return response
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Try again'
                }
                return make_response(jsonify(responseObject)), 500
            
@app.route("/main", methods=['GET'])
def f():
        # get the auth token
        auth_token = request.headers.get('Authorization')
        app.logger.info('AUTH TOKEN: ' + auth_token)
        if auth_token:
            status, resp = decode_auth_token(auth_token)
            if status == 'ok':
                # user = User.query.filter_by(id=resp).first()
                # responseObject = {
                #     'status': 'success',
                #     'data': {
                #         'user_id': user.id,
                #         'email': user.email,
                #         'admin': user.admin,
                #         'registered_on': user.registered_on
                #     }
                # }
                return make_response(), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

