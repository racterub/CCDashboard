#!/usr/bin/env python3


from app import app
from app.models import db
from app.models.tables import Users
from getpass import getpass

with app.app_context():
    name = input("Account Name: ")
    username = input("Username: ")
    password = getpass(prompt="Password: ")
    binance_api_key = input("Binance API Key: ")
    binance_api_secret = getpass(prompt="Binance API Secret: ")

    db.init_app(app)
    db.create_all()
    user = Users(
        username,
        password,
        name,
        binance_api_key,
        binance_api_secret,
    )
    db.session.add(user)
    db.session.commit()
