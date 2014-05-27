# -*- coding: utf-8 -*-

from __future__ import absolute_import

from papersplease import gpgauth
from wtforms import IntegerField


class GPGKeyIDField(IntegerField):

    """Like IntegerField, but handles/displays hex IDs."""

    def _value(self):
        if self.data is not None:
            return gpgauth.hex_key_id(self.data)
        else:
            return super(GPGKeyIDField, self)._value()

    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]
            if value.startswith('0x'):
                try:
                    self.data = int(value, 16)
                except ValueError:
                    self.data = None
                    raise ValueError(self.gettext('Not a valid hex value'))
            else:  # Fall back to IntegerField behavior.
                super(GPGKeyIDField, self).process_formdata(valuelist)
