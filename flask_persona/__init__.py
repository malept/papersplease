# -*- coding: utf-8 -*-

from . import views
from .blueprint import blueprint


def init_app(app, **kwargs):
    app.register_blueprint(blueprint, **kwargs)

__all__ = ('init_app', 'views')
