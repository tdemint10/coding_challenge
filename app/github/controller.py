from app.routes import app
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import Namespace, Resource

from .schema import GitHubProfileSchema
from .service import GithubService


api = Namespace("Github", description="GitHub Profile API")


# setup optional header
parser = api.parser()
parser.add_argument("X-GITHUB-TOKEN", location="headers")

# setup required args
parser.add_argument("organization", required=True, location="args")


@api.route("/profile")
@api.expect(parser)
class GithubResource(Resource):
    """ Github """

    @responds(schema=GitHubProfileSchema)
    def get(self) -> Response:
        """
        Get GitHub Profile
        """

        app.logger.info("GET GitHub Profile")

        args = parser.parse_args()
        res = GithubService.get_profile(args["X-GITHUB-TOKEN"], args["organization"])

        return res
