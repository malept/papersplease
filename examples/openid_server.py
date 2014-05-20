#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask.ext.script import Manager
from papersplease.flask_openid_idp import db, init_app

app = Flask(__name__)
# requires the following config values:
# * SECRET_KEY (see Flask config)
# * SQLALCHEMY_DATABASE_URI (see Flask-SQLAlchemy config)
app.config.from_object('local_settings')

init_app(app)
manager = Manager(app)


@manager.command
def createdb():
    """Creates database tables from SQLAlchemy models."""
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    manager.run()
