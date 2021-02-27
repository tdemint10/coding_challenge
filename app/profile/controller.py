from app.routes import app
from flask import jsonify, Response
from flask_restx import Namespace, Resource

from .service import GitProfileService


api = Namespace("GitProfile", description="Git Profile API")


@api.route("/github/<string:githubUsername>/bitbucket/<string:bitbucketUsername>")
@api.param("githubUsername", "GitHub Username")
@api.param("bitbucketUsername", "Bitbucket Username")
class GitProfileResource(Resource):
    """ Git Profile """

    def get(self, githubUsername, bitbucketUsername):
        """
        Get Git Profile
        """

        app.logger.info("Get Git Profile")

        res = GitProfileService.get_profile(githubUsername, bitbucketUsername)

        return jsonify(res)
