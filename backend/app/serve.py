#!/usr/bin/env python3


from app import app
from app.models import db

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
