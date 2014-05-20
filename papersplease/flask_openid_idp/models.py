# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from functools import partial
from openid.association import Association
from openid.store import nonce as oid_nonce
from openid.store.interface import OpenIDStore as BaseOpenIDStore
from operator import attrgetter
from sqlalchemy.exc import IntegrityError
from time import time

db = SQLAlchemy()
PKColumn = partial(db.Column, nullable=False, primary_key=True)


class OpenIDAssociation(db.Model):
    __tablename__ = 'openid_associations'

    server_url = PKColumn(db.String(2047))
    handle = PKColumn(db.String(255))
    secret = db.Column(db.LargeBinary(128), nullable=False)
    issued = db.Column(db.Integer, nullable=False)
    lifetime = db.Column(db.Integer, nullable=False)
    assoc_type = db.Column(db.String(64), nullable=False)


class OpenIDNonce(db.Model):
    __tablename__ = 'openid_nonces'
    __table_args__ = (
        db.UniqueConstraint('server_url', 'timestamp', 'salt'),
    )

    server_url = PKColumn(db.String(2047))
    timestamp = PKColumn(db.Integer)
    salt = PKColumn(db.CHAR(40))


class OpenIDStore(BaseOpenIDStore):

    def association_query(self, server_url, handle=None):
        query = OpenIDAssociation.query.filter_by(server_url=server_url)
        if handle:
            query = query.filter_by(handle=handle)
        return query

    def storeAssociation(self, server_url, assoc):
        association = OpenIDAssociation(server_url=server_url,
                                        handle=assoc.handle,
                                        secret=assoc.secret,
                                        issued=assoc.issued,
                                        lifetime=assoc.lifetime,
                                        assoc_type=assoc.assoc_type)
        db.session.add(association)
        db.session.commit()

    def getAssociation(self, server_url, handle=None):
        db_assocs = self.association_query(server_url, handle).all()
        assocs = [Association(a.handle, a.secret, a.issued, a.lifetime,
                              a.assoc_type)
                  for a in db_assocs]
        if assocs:
            assocs.sort(key=attrgetter('issued'), reverse=True)
            return assocs[0]
        else:
            return None

    def removeAssociation(self, server_url, handle):
        return self.association_query(server_url, handle).delete() > 0

    def useNonce(self, server_url, timestamp, salt):
        if abs(timestamp - time.time()) > oid_nonce.SKEW:
            return False
        nonce = OpenIDNonce(server_url=server_url, timestamp=timestamp,
                            salt=salt)
        db.session.add(nonce)
        try:
            db.session.commit()
        except IntegrityError:
            return False
        else:
            return True

    def cleanupNonces(self):
        ts_constraint = OpenIDNonce.timestamp < int(time() - oid_nonce.SKEW)
        return OpenIDNonce.query.filter(ts_constraint).delete()

    def cleanupAssociations(self):
        issued_constraint = \
            OpenIDAssociation.issued + OpenIDAssociation.lifetime < time()
        return OpenIDAssociation.query.filter(issued_constraint).delete()
