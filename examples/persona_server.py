#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask.ext.script import Manager
from papersplease.flask_persona import init_app, manager as persona_mgr

app = Flask(__name__)
app.config.from_object('local_settings')

manager = Manager(app)
manager.add_command('persona', persona_mgr)

init_app(app)

if __name__ == '__main__':
    manager.run()
