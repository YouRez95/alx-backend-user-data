#!/usr/bin/env python3
'''
    flask app
'''

from flask import Flask, abort, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")