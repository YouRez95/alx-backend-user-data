#!/usr/bin/env python3
""" Module of Session_auth views
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_route() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - login the user, respond with session id
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})
    except KeyError:
        return None

    if not user or not user[0]:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    out = jsonify(user[0].to_json())
    out.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return out


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ GET /api/v1/auth_session/logout
    Return:
      - delete the sessionId
    """
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)
    if is_deleted is False:
        abort(404)
    return jsonify({}), 200
