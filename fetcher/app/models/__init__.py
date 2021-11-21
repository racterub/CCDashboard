#!/usr/bin/env python3

import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker

DBURL = os.environ.get('DBURL')
# DBURL = "mysql+pymysql://root:James50428@localhost/ccdashboard?charset=utf8mb4"

engine = sqlalchemy.create_engine(DBURL)
db = sessionmaker(engine)

from models.tables import *