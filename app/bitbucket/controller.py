from app.routes import app
from flask import Response
from flask_restx import Namespace, Resource


api = Namespace("Bitbucket", description="Bitbucket Profile API")


@api.route("/")
class BitbucketResource(Resource):
    """ Bitbucket """

    def get(self):
        """
        Endpoint for Bitbucket
        """

        app.logger.info("Bitbucket endpoint")
        return Response("Bitbucket", status=200)
