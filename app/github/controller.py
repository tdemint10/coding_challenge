from app.routes import app
from flask import Response
from flask_restx import Namespace, Resource


api = Namespace("Github", description="GitHub Profile API")


@api.route("/")
class GithubResource(Resource):
    """ Github """

    def get(self):
        """
        Endpoint for GitHub
        """

        app.logger.info("Github endpoint")
        return Response("Github", status=200)
