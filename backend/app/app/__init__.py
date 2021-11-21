#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from datetime import datetime, timezone, timedelta
from .models import db
from .models.tables import Users


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.
    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }
    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
# app.config.from_object('config.devConfig')
app.config.from_object('config.prodConfig')
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=24))
        if target_timestamp > exp_timestamp:
            user = Users.query.filter_by(id=get_jwt_identity()).one_or_none()
            access_token = create_access_token(identity=user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

## Override callbacks with customized return messages.
@jwt.invalid_token_loader
def invalid_token_callback(data):
    resp = jsonify({
        "status": False,
        "auth": True,
        "msg": "Invalid token."
    })
    unset_jwt_cookies(resp)
    return resp

@jwt.token_verification_failed_loader
def token_verification_failed_callback(a, b):
    resp = jsonify({
        "status": False,
        "auth": True,
        "msg": "Token verification failed."
    })
    unset_jwt_cookies(resp)
    return resp

@jwt.unauthorized_loader
def unauthorized_callback(data):
    resp = jsonify({
        "status": False,
        "auth": True,
        "msg": "Unauthorized."
    })
    unset_jwt_cookies(resp)
    return resp

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    resp = jsonify({
        "status": False,
        "auth": True,
        "msg": "Token expired."
    })
    unset_jwt_cookies(resp)
    return resp

@jwt.revoked_token_loader
def provoked_token_callback(jwt_header, jwt_payload):
    resp = jsonify({
        "status": False,
        "auth": True,
        "msg": "Token expired."
    })
    unset_jwt_cookies(resp)
    return resp

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()

from .views.auth import auth
from .views.api import api
from .views.settings import settings

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/service')
app.register_blueprint(settings, url_prefix='/settings')
