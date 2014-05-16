#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, url_for
from flask.ext.script import Command, Manager, Option
from papersplease import persona
from papersplease.flask_persona import init_app

app = Flask(__name__)
app.config.from_object('local_settings')
manager = Manager(app)
init_app(app)


def add_command(cmd_class):
    manager.add_command(cmd_class.name, cmd_class())
    return cmd_class


@add_command
class GenerateWellKnown(Command):
    '''Generates the JSON for /.well-known/browserid.'''

    name = 'generate-wellknown'

    option_list = (
        Option('-o', '--output-dir', default=None),
    )

    def run(self, output_dir):
        auth_url = url_for('persona_signin')
        provisioning_url = url_for('persona_provisioning')
        persona.generate_wellknown_files(auth_url, provisioning_url,
                                         output_dir)

if __name__ == '__main__':
    manager.run()