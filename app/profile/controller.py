from app.routes import app
from flask import Response
from flask_restx import Namespace, Resource


api = Namespace("Profile", description="Profile API")


@api.route("/")
class ProfileResource(Resource):
    """ Profile """

    def get(self):
        """
        Endpoint for Profile
        """

        app.logger.info("Profile endpoint")
        return Response("Profile", status=200)
