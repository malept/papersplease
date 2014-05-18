#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask.ext.script import Manager
from papersplease.flask_openid_idp import db, init_app

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/openid.db'

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
