#!/usr/bin/env python3
"""
Route module for the api
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Unauthorized hansler """
    return jsonify({"error": "Unauthorized"}), 401
