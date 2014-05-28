# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.script import Command, Manager, Option
from papersplease import persona
from papersplease.flask_script import script_command

DESC = 'Perform Persona-related operations.'

manager = Manager(description=DESC, help=DESC)


@script_command(manager)
class GenerateWellKnown(Command):
    """Generate the JSON for /.well-known/browserid."""

    name = 'generate-wellknown'

    option_list = (
        Option('-o', '--output-dir', default=None),
    )

    def run(self, output_dir):
        auth_url = url_for('persona_signin')
        provisioning_url = url_for('persona_provisioning')
        persona.generate_wellknown_files(auth_url, provisioning_url,
                                         output_dir)
