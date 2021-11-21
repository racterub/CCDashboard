#!/usr/bin/env python3

from app.models import db
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

class Spots(db.Model):
    __tablename__ = 'spots'
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(5))
    base = db.Column(db.String(5))
    amount = db.Column(db.Float)
    uamount = db.Column(db.Float)
    commission = db.Column(db.Float)
    commission_type = db.Column(db.String(5))
    tx_type = db.Column(db.Boolean)
    buy_price = db.Column(db.Float)
    trade_time = db.Column(db.DateTime)

    def __init__(self, coin, base, amount, uamount, commission, commission_type, tx_type, buy_price, trade_time):
        self.coin = coin
        self.base = base
        self.amount = amount
        self.uamount = uamount
        self.commission = commission
        self.commission_type = commission_type
        self.tx_type = tx_type
        self.buy_price = buy_price
        self.trade_time = trade_time
    
    def __repr__(self):
        return f"<Spots: Pair '{self.coin}{self.base}', BuyPrice: {self.buy_price}>"


class Summary(db.Model):
    __tablename__ = 'summary'
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(5)) # coin name
    change = db.Column(db.Float)
    cost = db.Column(db.Float) # coin cost based on how much USDT do you use to buy this amount of coin
    amount = db.Column(db.Float) # coin quantity
    uamount = db.Column(db.Float) # coin value in STABLE COIN (USD)
    current_price = db.Column(db.Float) # coin's current price

    def __init__(self, coin, change, cost, amount, uamount, current_price):
        self.coin = coin
        self.change = change
        self.cost = cost
        self.amount = amount
        self.uamount = uamount
        self.current_price = current_price
    
    def __repr__(self):
        return f"<Summary: Coin '{self.coin}', Amount: {self.amount}>"

class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    id = db.Column(db.Integer, primary_key=True)
    change = db.Column(db.Float)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, change):
        self.change = change
    
    def __repr__(self):
        return f"<Dashboard: Change '{self.change}'"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    api_key = db.Column(db.Text, nullable=False)
    api_secret = db.Column(db.Text, nullable=False)


    def __init__(self, username, password, name, api_key, api_secret, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_new_password_hash(self, new_password):
        return generate_password_hash(new_password)

    def __repr__(self):
        return f"<Users: username: {self.username}, name: {self.name}>"