from app.routes import app
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import Namespace, Resource

from .schema import BitbucketProfileSchema
from .service import BitbucketService


api = Namespace("Bitbucket", description="Bitbucket Profile API")


@api.route("/<string:profileName>")
@api.param("profileName", "Profile Name")
class BitbucketResource(Resource):
    """ Bitbucket """

    @responds(schema=BitbucketProfileSchema)
    def get(self, profileName):
        """
        Get Bitbucket Profile
        """

        app.logger.info("GET Bitbucket Profile")

        res = BitbucketService.get_profile(profileName)

        return res
