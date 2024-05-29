#!/usr/bin/env python3
'''
    flask app
'''

from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
