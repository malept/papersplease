# -*- coding: utf-8 -*-

from .blueprint import blueprint
from .models import db
from .views import login_manager


def init_app(app, **kwargs):
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(blueprint, **kwargs)
