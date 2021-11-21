#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from app.models import db
from app.models.tables import Users
from .exchanges.Binance import Binance

settings = Blueprint("settings", __name__)

@settings.route("/updatePassword", methods=["POST"])
@jwt_required()
def reset_password():
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    if (not old_password and not new_password):
        return jsonify({
            "status": False,
            "msg": "Invalid data."
        })
    
    user = Users.query.filter_by(username=current_user.username).first()
    if (user.verify_password(old_password)):
        user.password = user.generate_new_password_hash(new_password)
        db.session.commit()
        return jsonify({
            "status": True,
            "msg": "Password successfully updated."
        })
    else:
        return jsonify({
            "status": False,
            "msg": "Invalid old password."
        })

@settings.route("/updateBinance", methods=["POST"])
@jwt_required()
def update_binance():
    new_api_key = request.form.get('newAPIKey')
    new_api_secret = request.form.get('newAPISecret')

    user = Users.query.filter_by(username=current_user.username).first()
    client = Binance(new_api_key, new_api_secret)
    if (client.check_account_status()):
        user.api_key = new_api_key
        user.api_secret = new_api_secret
        db.session.commit()
        return jsonify({
            "status": True,
            "msg": "API successfully updated."
        })
    else:
        return jsonify({
            "status": False,
            "msg": "Invalid API credentials."
        })

@settings.route("/checkAccountStatus")
@jwt_required()
def check_account_status():
    user = Users.query.filter_by(username=current_user.username).first()
    client = Binance(user.api_key, user.api_secret)
    if (client.check_account_status()):
        return jsonify({
            "status": True,
            "msg": "Account normal."
        })
    else:
        return jsonify({
            "status": False,
            "msg": "Account abnormal."
        })