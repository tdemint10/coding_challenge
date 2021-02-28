from app.routes import app
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import Namespace, Resource

from .schema import BitbucketProfileSchema
from .service import BitbucketService


api = Namespace("Bitbucket", description="Bitbucket Profile API")

# setup required args
parser = api.parser()
parser.add_argument("team", required=True, location="args")


@api.route("/profile")
@api.expect(parser)
class BitbucketResource(Resource):
    """ Bitbucket """

    @responds(schema=BitbucketProfileSchema)
    def get(self):
        """
        Get Bitbucket Profile
        """

        app.logger.info("GET Bitbucket Profile")

        args = parser.parse_args()
        res = BitbucketService.get_profile(args["team"])

        return res
