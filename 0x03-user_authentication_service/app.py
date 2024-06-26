#!/usr/bin/env python3
'''
    flask app
'''

from flask import Flask, abort, jsonify, redirect, request
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def hello_world():
    '''
      home route
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    '''
        route that can register user
        form data required:
            email, password
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    '''
        route that can login user  and add sessionid to coockies
        form data required:
            email, password
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    valid_credentials = AUTH.valid_login(email, password)
    if not valid_credentials:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''
        route that can logout user
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    '''
        route that can get the credentials of user
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''
        reset password token
    '''
    email = request.form.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''
        update password
    '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
