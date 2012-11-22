#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.script import Command, Manager, Option
from flask_persona import app
import papersplease

manager = Manager(app)


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
        papersplease.generate_wellknown_files(auth_url, provisioning_url,
                                              output_dir)

if __name__ == '__main__':
    manager.run()
