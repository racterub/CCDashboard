#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from app.models.tables import Users, Spots
from app.models import db
from .fetcher.fetcher import fetch_binance_data

auth = Blueprint('auth', __name__)

# NOPE
# NOT NOW
# @auth.route("/signup", methods=['POST'])
# def signup():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     name = request.form.get("name")

#     if Users.query.filter_by(username=username).count():
#         return jsonify({
#             "status": False,
#             "msg": "Username has already taken."
#         })
#     user = Users(username, password, name)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({
#         "status": True,
#         "msg": "Signup successfully."
#     })



@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = Users.query.filter_by(username=username).first()
    if (user and user.verify_password(password)):
        if (Spots.query.count() == 0) :
            # First time login
            fetch_binance_data(user.api_key, user.api_secret)
        resp = jsonify({
            "status": True,
            "name": user.name,
            "msg": "Logged in."
        })
        print(f"login: {user}")
        set_access_cookies(resp, create_access_token(identity=user))
        return resp
    else:
        return jsonify({
            "status": False,
            "msg": "Invalid username or password."
        })

@auth.route("/logout")
@jwt_required()
def logout():
    resp = jsonify({
        "status": True,
        "msg": "Logged out."
    })
    unset_jwt_cookies(resp)
    return resp, 200


