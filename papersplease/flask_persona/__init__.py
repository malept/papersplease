# -*- coding: utf-8 -*-

from . import views
from .blueprint import blueprint
try:
    from .script import manager
except ImportError:
    manager = None


def init_app(app, **kwargs):
    app.register_blueprint(blueprint, **kwargs)

__all__ = ('init_app', 'manager', 'views')
