#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask.ext.script import Manager
from papersplease.flask_persona import init_app, manager as persona_mgr

app = Flask(__name__)
# requires the following config values:
# * PERSONA_DOMAIN - the domain name that the IdP represents
# * PERSONA_PRIVATE_KEY_FILENAME - the absolute path to the IdP's private key
app.config.from_object('local_settings')

manager = Manager(app)
manager.add_command('persona', persona_mgr)

init_app(app)

if __name__ == '__main__':
    manager.run()
