from flask import Flask, request, make_response, jsonify, abort
from hashlib import sha256
from login.login_service import _build_cors_preflight_response, _corsify_actual_response, encode_auth_token, decode_auth_token, authenticate, is_authorized
import pymongo
import yaml
import sys
import os
import datetime
import jwt
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route("/login", methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
        return authenticate(request)
            
@app.route("/main", methods=['GET'])
def f():
    if is_authorized(request):
        return make_response(), 200

