#!/usr/bin/env python3
""" Basic flask app """

from flask import Flask, jsonify, request
from auth import Auth


Auth = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """ webapp hompage / index """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    email = request.form["email"]
    password = request.form["password"]

    try:
        user = Auth.register_user(email, password)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
