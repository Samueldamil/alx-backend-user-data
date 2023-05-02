#!/usr/bin/env python3
""" Module for index """
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized', method=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized """
    abort(401)
