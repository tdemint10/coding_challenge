from app.routes import app
from flask import jsonify, Response
from flask_restx import Namespace, Resource

from .service import GithubService


api = Namespace("Github", description="GitHub Profile API")


# setup optional header
parser = api.parser()
parser.add_argument('X-GITHUB-TOKEN', location='headers')


@api.route("/<string:profileName>")
@api.param("profileName", "Profile Name")
@api.expect(parser)
class GithubResource(Resource):
    """ Github """

    def get(self, profileName: str) -> Response:
        """
        Get GitHub Profile
        """

        app.logger.info("GET GitHub Profile")

        args = parser.parse_args()
        res = GithubService.get_profile(args["X-GITHUB-TOKEN"], profileName)

        return res
