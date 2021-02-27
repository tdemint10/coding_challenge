import logging

import flask
from flask import Response
from flask_restx import Api

from app.github import register_routes as attach_github
from app.bitbucket import register_routes as attach_bitbucket
from app.profile import register_routes as attach_profile

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)
api = Api(app, title="Git Profile API", version="0.0.1")


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/teapot", methods=["GET"])
def teapot():
    """
    Endpoint to check for a teapot
    """
    app.logger.info("I'm a teapot")
    return Response("I'm a teapot", status=418)


attach_github(api, app)
attach_bitbucket(api, app)
attach_profile(api, app)
