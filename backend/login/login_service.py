from flask import Flask, request, make_response, jsonify, abort
from hashlib import sha256
import datetime
import jwt


SECRET_KEY="secret"   

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
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
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
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return 'ok', payload['sub']
    except jwt.ExpiredSignatureError:
        return 'err', 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'err', 'Invalid token. Please log in again.'
    
def authenticate(collection, username, password):
        encoded_password = sha256(password.encode('UTF-8')).hexdigest()
        user_db = collection.find_one({'username': username})
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
            
def is_authorized(request):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            status, resp = decode_auth_token(auth_token)
            return status == 'ok', resp