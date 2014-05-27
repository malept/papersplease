# -*- coding: utf-8 -*-

from papersplease import gpgauth
from sqlalchemy import BigInteger, Column
from sqlalchemy.ext.declarative import declared_attr


class GPGAuthMixin(object):

    """SQLAlchemy model mixin for OpenGPG key IDs."""

    @declared_attr
    def openpgp_key_id(cls):
        return Column(BigInteger, nullable=False)

    @staticmethod
    def import_remote_key(mapper, connection, target, gpg,
                          keyserver='pgp.mit.edu'):
        gpgauth.import_key_from_server(keyserver, target.openpgp_key_id,
                                       gpg=gpg)
