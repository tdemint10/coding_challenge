from app.routes import app
from flask import jsonify, Response
from flask_restx import Namespace, Resource

from .service import GitProfileService


api = Namespace("GitProfile", description="Git Profile API")

# setup optional header
parser = api.parser()
parser.add_argument('X-GITHUB-TOKEN', location='headers')


@api.route("/github/<string:githubUsername>/bitbucket/<string:bitbucketUsername>")
@api.param("githubUsername", "GitHub Username")
@api.param("bitbucketUsername", "Bitbucket Username")
@api.expect(parser)
class GitProfileResource(Resource):
    """ Git Profile """

    def get(self, githubUsername, bitbucketUsername):
        """
        Get Git Profile
        """

        app.logger.info("Get Git Profile")

        args = parser.parse_args()
        res = GitProfileService.get_profile(args["X-GITHUB-TOKEN"], githubUsername, bitbucketUsername)

        return jsonify(res)
