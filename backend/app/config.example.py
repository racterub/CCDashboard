#!/usr/bin/env python3


import secrets
from datetime import timedelta
import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class devConfig(BaseConfig):
    DEBUG = True
    JWT_SECRET_KEY = "TEST"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

class prodConfig(BaseConfig):
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get("SECRETKEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DBURL")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)