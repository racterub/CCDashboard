#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Spots(Base):
    __tablename__ = 'spots'
    id = Column(Integer, primary_key=True)
    coin = Column(String(5))
    base = Column(String(5))
    amount = Column(Float)
    uamount = Column(Float)
    commission = Column(Float)
    commission_type = Column(String(5))
    tx_type = Column(Boolean)
    buy_price = Column(Float)
    trade_time = Column(DateTime)

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


class Summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True)
    coin = Column(String(5)) # coin name
    cost = Column(Float) # coin cost based on how much USDT do you use to buy this amount of coin
    change = Column(Float) # coin profit/lost based on current price
    amount = Column(Float) # coin quantity
    uamount = Column(Float) # coin value in STABLE COIN (USD)
    current_price = Column(Float) # coin's current price

    def __init__(self, coin, change, cost, amount, uamount, current_price):
        self.coin = coin
        self.cost = cost
        self.change = change
        self.amount = amount
        self.uamount = uamount
        self.current_price = current_price
    
    def __repr__(self):
        return f"<Summary: Coin '{self.coin}', Amount: {self.amount}>"

class Dashboard(Base):
    __tablename__ = 'dashboard'
    id = Column(Integer, primary_key=True)
    change = Column(Float)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, change):
        self.change = change
    
    def __repr__(self):
        return f"<Dashboard:  Change '{self.change}'"

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    api_key = Column(Text)
    api_secret = Column(Text)
    """
    Future changes: Support multiple users
    db relation to the record is needed
    """

    def __repr__(self):
        return f"<Users: username: {self.username}, name: {self.name}>"