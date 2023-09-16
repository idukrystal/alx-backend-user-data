#!/usr/bin/env python3
""" Basic flask app """

from flask import Flask, abort, jsonify, redirect, make_response, request
from auth import Auth


AUTH = Auth()
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
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password):
        uid = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", uid)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    session_id = request.cookies.get("session_id", None)
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
