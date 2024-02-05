from flask import Flask, request, make_response, jsonify
from hashlib import sha256
from login.login_service import _build_cors_preflight_response, authenticate, is_authorized, decode_auth_token
from preference.preference_service import get_preferences_for_user, update_preferences_for_user
from query.query_service import query_by_origins
from flask_cors import CORS
import pymongo
import yaml
import sys
import os

app = Flask(__name__)
cors = CORS(app)

os.chdir(r'C:\Users\eniav\Desktop\WADe-Web-Developer-Companion\backend')

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

try:
    client = pymongo.MongoClient(config['db']['db_url'], server_api=pymongo.server_api.ServerApi(config['db']['db_server_api']))
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.WDC
user_collection = db['users']
preference_collection = db['preferences']

@app.route("/login", methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
        username = request.args.get('username','')
        password = request.args.get('password','')
        return authenticate(user_collection, username, password)


@app.route("/main", methods=['GET'])
def access_main():
    if is_authorized(request):
        return make_response(), 200
    else:
        return make_response(), 401


@app.route("/preferences", methods=['GET', 'OPTIONS'])
def get_preferences_for_current_user():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
        if is_authorized(request):
            auth_token = request.headers.get('Authorization')
            status, username = decode_auth_token(auth_token)
            preferences = get_preferences_for_user(preference_collection, username)
            response = jsonify({
                "owner_username": preferences['owner_username'],
                "origins": preferences['origins'],
                "topics": preferences['topics']
            })
            return response, 200
        else:
            return make_response(), 401
        

@app.route("/preferences", methods=['POST', 'OPTIONS'])
def update_preferences_for_current_user():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
        if is_authorized(request):
            auth_token = request.headers.get('Authorization')
            status, username = decode_auth_token(auth_token)
            selected_sources = request.json['selected_sources']
            new_preferences = update_preferences_for_user(preference_collection, username, selected_sources)
            if new_preferences:
                content = query_by_origins(new_preferences['origins'])
                app.logger.info(content)
                return content, 200
            else:
                return make_response(), 400
            

