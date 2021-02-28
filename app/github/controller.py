from app.routes import app
from app.exceptions import ForbiddenException
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import fields, Namespace, Resource

from .schema import GitHubProfileSchema
from .service import GithubService


api = Namespace("Github", description="GitHub Profile API")

# create response model for docs
response_model = api.model("GithubProfile", {
    "followerCount": fields.Integer,
    "repoCount": fields.Integer,
    "originalRepoCount": fields.Integer,
    "forkedRepoCount": fields.Integer,
    "languages": fields.List(fields.String),
    "topics": fields.List(fields.String),
    "watchersCount": fields.Integer
})

# header/argument parser for incoming requests
parser = api.parser()
parser.add_argument("X-GITHUB-TOKEN", location="headers")
parser.add_argument("organization", required=True, location="args")


@api.route("/profile")
class GithubResource(Resource):
    """ Github """

    @api.expect(parser)
    @api.response(200, "Success", response_model)
    @api.doc(responses={
        400: "Bad Request",
        403: "Forbidden",
        500: "Internal Error"
    })
    @responds(schema=GitHubProfileSchema)
    def get(self) -> Response:
        """
        Get GitHub Profile
        """

        app.logger.info("GET GitHub Profile")

        # retrieve args
        args = parser.parse_args()

        # try to build the GithubProfile and return correct status
        try:
            return GithubService.get_profile(args["X-GITHUB-TOKEN"], args["organization"])
        except ForbiddenException as err:
            return Response(f"ERROR - {err}", status=403)
        except Exception as err:
            return Response(f"ERROR - {err}", status=500)
