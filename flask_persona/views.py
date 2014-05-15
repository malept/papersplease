# -*- coding: utf-8 -*-

from flask import render_template, request
from papersplease.persona import generate_identity_cert, sign_as_rsa_jws
from . import app


@app.route('/signin')
def persona_signin():
    return render_template('signin.html')


@app.route('/provisioning')
def persona_provisioning():
    return render_template('provisioning.html')


@app.route('/generate-cert', methods=['POST'])
def persona_generate_certificate():
    '''
    See: https://github.com/mozilla/browserid-certifier
    '''
    email = request.json['email']
    #TODO assert that email is a valid principal

    cert = generate_identity_cert(app.config['PERSONA_DOMAIN'],
                                  email,
                                  request.json['cert_duration'],
                                  request.json['public_key'])
    key = None
    with open(app.config['PERSONA_PRIVATE_KEY_FILENAME']) as f:
        key = f.read()
    return sign_as_rsa_jws(key, cert)


@app.route('/.well-known/browserid')
def persona_browserid():
    result = app.send_static_file('browserid')
    result.content_type = 'application/json'
    return result
