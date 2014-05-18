# -*- coding: utf-8 -*-

from flask import make_response, render_template, request, url_for
from flask.ext.login import current_user, LoginManager
from openid.server.server import (
    EncodingError, ProtocolError, Server as OpenIDServer)
from .blueprint import blueprint
from .models import OpenIDStore

ERROR_TPL = 'papersplease/openid/error.html'

login_manager = LoginManager()


def openid_exception(err):
    return make_response(render_template(ERROR_TPL, error=err), 400)


def openid_response(openid, oid_resp):
    try:
        oid_webresp = openid.encodeResponse(oid_resp)
        resp = make_response(oid_webresp.body, oid_webresp.code)
    except EncodingError as e:
        return openid_exception(e)
    else:
        for k, v in oid_webresp.headers.iteritems():
            resp.headers.add_header(k, v)
        return resp


@blueprint.route('/openid', methods=['GET', 'POST'])
def endpoint():
    endpoint_url = url_for('.endpoint', _external=True)
    openid = OpenIDServer(OpenIDStore(), endpoint_url)
    query = request.args if request.method == 'GET' else request.form
    try:
        oid_req = openid.decodeRequest(query)
    except ProtocolError as e:
        return openid_exception(e)
    if not oid_req:
        return render_template('papersplease/openid/index.html')
    if oid_req.mode in ('checkid_immediate', 'checkid_setup'):
        if current_user.is_authenticated():
            return openid_response(openid, oid_req.answer(True))
        elif oid_req.immediate:
            return openid_response(openid, oid_req.answer(False))
        else:
            return login_manager.unauthorized()
    else:
        return openid_response(openid, openid.handleRequest(oid_req))
