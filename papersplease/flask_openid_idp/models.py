# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from functools import partial
from openid.association import Association
from openid.store import nonce as oid_nonce
from openid.store.interface import OpenIDStore as BaseOpenIDStore
from operator import attrgetter
from sqlalchemy import (
    CHAR, Column, Integer, LargeBinary, String, UniqueConstraint)
from sqlalchemy.exc import IntegrityError
from time import time

PKColumn = partial(Column, nullable=False, primary_key=True)
db = SQLAlchemy()


class OpenIDAssociation(db.Model):
    __tablename__ = 'openid_association'

    server_url = PKColumn(String(2047))
    handle = PKColumn(String(255))
    secret = Column(LargeBinary(128), nullable=False)
    issued = Column(Integer, nullable=False)
    lifetime = Column(Integer, nullable=False)
    assoc_type = Column(String(64), nullable=False)


class OpenIDNonce(db.Model):
    __tablename__ = 'openid_nonce'
    __table_args__ = (
        UniqueConstraint('server_url', 'timestamp', 'salt'),
    )

    server_url = PKColumn(String(2047))
    timestamp = PKColumn(Integer)
    salt = PKColumn(CHAR(40))


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
