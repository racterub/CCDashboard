#!/usr/bin/env python3

import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os

DBURL = os.environ.get("DBURL")
# DBURL = "mysql+pymysql://root:James50428@localhost/ccdashboard?charset=utf8mb4"

engine = sqlalchemy.create_engine(DBURL)
db = sessionmaker(engine)

from .tables import *
