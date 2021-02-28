from app.routes import app
from app.exceptions import ForbiddenException
from flask import jsonify, Response
from flask_accepts import responds
from flask_restx import Namespace, Resource

from .schema import GitProfileSchema
from .service import GitProfileService


api = Namespace("GitProfile", description="Git Profile API")

# header/argument parser for incoming requests
parser = api.parser()
parser.add_argument("X-GITHUB-TOKEN", location="headers")
parser.add_argument("githubOrganization", required=True, location="args")
parser.add_argument("bitbucketTeam", required=True, location="args")


@api.route("/")
class GitProfileResource(Resource):
    """ Git Profile """

    @api.expect(parser)
    @responds(schema=GitProfileSchema)
    def get(self):
        """
        Get Git Profile
        """

        app.logger.info("Get Git Profile")

        # retrieve args
        args = parser.parse_args()

        # try to build the GithubProfile and return correct status
        try:
            return GitProfileService.get_profile(args["X-GITHUB-TOKEN"], args["githubOrganization"], args["bitbucketTeam"])
        except ForbiddenException as err:
            return Response(f"ERROR - {err}", status=403)
        except Exception as err:
            return Response(f"ERROR - {err}", status=500)
