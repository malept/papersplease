# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('local_settings')

import views

__all__ = ['app', 'views']
