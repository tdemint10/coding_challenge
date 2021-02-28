from app.routes import app
from app.exceptions import ForbiddenException
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import fields, Namespace, Resource

from .schema import BitbucketProfileSchema
from .service import BitbucketService


api = Namespace("Bitbucket", description="Bitbucket Profile API")

# create response model for docs
response_model = api.model("BitbucketProfile", {
    "followerCount": fields.Integer,
    "repoCount": fields.Integer,
    "languages": fields.List(fields.String),
    "watchersCount": fields.Integer
})

# argument parser for incoming requests
parser = api.parser()
parser.add_argument("team", required=True, location="args")


@api.route("/profile")
class BitbucketResource(Resource):
    """ Bitbucket """

    @api.expect(parser)
    @api.response(200, "Success", response_model)
    @api.doc(responses={
        400: "Bad Request",
        403: "Forbidden",
        500: "Internal Error"
    })
    @responds(schema=BitbucketProfileSchema)
    def get(self):
        """
        Get Bitbucket Profile
        """

        app.logger.info("GET Bitbucket Profile")

        # retrieve args
        args = parser.parse_args()

        # try to build the BitbucketProfile and return correct status
        try:
            return BitbucketService.get_profile(args["team"])
        except ForbiddenException as err:
            return Response(f"ERROR - {err}", status=403)
        except Exception as err:
            return Response(f"ERROR - {err}", status=500)
