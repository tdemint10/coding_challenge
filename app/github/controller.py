from app.routes import app
from flask import jsonify, Response
from flask_restx import Namespace, Resource

from .service import GithubService


api = Namespace("Github", description="GitHub Profile API")


@api.route("/<string:profileName>")
@api.param("profileName", "Profile Name")
class GithubResource(Resource):
    """ Github """

    def get(self, profileName: str) -> Response:
        """
        Get GitHub Profile
        """

        app.logger.info("GET GitHub Profile")

        res = GithubService.get_github_profile(profileName)

        return jsonify(res)
