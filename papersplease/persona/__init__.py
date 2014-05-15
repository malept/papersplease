# -*- coding: utf-8 -*-

from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto import Random
import hashlib
try:
    import simplejson as json
except ImportError:
    import json
import os

KEY_ALGORITHM = 'RS256'


def generate_identity_cert(issuing_domain, email, duration, public_key):
    twenty_four_hours_in_seconds = 24 * 60 * 60
    # The backend server MUST NOT issue a certificate valid longer than
    # 24 hours.
    cert_duration = min(twenty_four_hours_in_seconds, duration)
    cert = {
        'iss': issuing_domain,
        'exp': cert_duration,
        'public-key': public_key,
        'principal': {
            'email': email,
        },
    }
    return json.dumps(cert, separators=(',', ':'))


def sign_as_rsa_jws(private_key, data):
    '''Helper function to generate a JSON Web Signature (JWS) for a given
    RSA key and payload.

    See also:
    http://self-issued.info/docs/draft-ietf-jose-json-web-signature.html
    '''
    header = b64encode(json.dumps({'alg': KEY_ALGORITHM}))
    payload = b64encode(data)
    key = RSA.importKey(private_key)
    data_hash = hashlib.md5(data).digest()
    signature = key.sign(data_hash, None)[0]
    return '.'.join([header, payload, str(signature)])


def generate_wellknown_files(auth_url, provisioning_url, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    rsa_key = RSA.generate(2048, Random.new().read)
    with open(os.path.join(output_dir, 'persona.pem'), 'w') as f:
        f.write(rsa_key.exportKey('PEM'))
    data = {
        'public-key': {
            'algorithm': KEY_ALGORITHM[:2], # XXX jwcrypto doesn't support RS256??
            'n': str(rsa_key.n),
            'e': str(rsa_key.e),
        },
        'authentication': auth_url,
        'provisioning': provisioning_url,
    }
    with open(os.path.join(output_dir, 'browserid'), 'w') as f:
        json.dump(data, f)
