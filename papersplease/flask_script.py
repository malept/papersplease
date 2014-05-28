# -*- coding: utf-8 -*-
"""Flask-Script helpers."""


def script_command(manager):
    """
    Decorator to create Flask-Script commands from Command-derived classes.

    :param flask.ext.script.Manager manager: The manager instance to attach the
                                             command to.
    """

    def add_command(cls):
        manager.add_command(cls.name, cls())
        return cls
    return add_command
