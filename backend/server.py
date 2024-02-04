from flask import Flask, request, make_response
from hashlib import sha256
from login.login_service import _build_cors_preflight_response, authenticate, is_authorized
from flask_cors import CORS

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

