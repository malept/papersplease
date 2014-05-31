# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    from flask.ext.babelex import lazy_gettext as _
except ImportError:
    from flask.ext.babel import lazy_gettext as _
from papersplease import gpgauth
from .wtforms import GPGKeyIDField


class GPGAuthAdminViewMixin(object):
    form_overrides = {
        'openpgp_key_id': GPGKeyIDField,
    }
    form_args = {
        'openpgp_key_id': {
            'label': _(u'OpenPGP Key ID'),
        }
    }
    column_labels = {
        'openpgp_key_id': _(u'OpenPGP Key ID'),
    }
    column_formatters = {
        'openpgp_key_id': lambda v, c, m, p:
            gpgauth.hex_key_id(m.openpgp_key_id),
    }
