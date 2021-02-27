from app.routes import app
from app.github.service import GithubService
from app.bitbucket.service import BitbucketService


class GitProfileService:
    @staticmethod
    def get_profile(github_token: str, github_user: str, bitbucket_user: str):
        app.logger.info(f"GitProfileService - get_profile - github_user: {github_user}, bitbucket_user: {bitbucket_user}")

        # create profile object to return
        profile = GitProfileService.create_profile()

        # get individual profiles from services
        github_profile = GithubService.get_profile(github_token, github_user)
        bitbucket_profile = BitbucketService.get_profile(bitbucket_user)

        # combine profiles
        GitProfileService.add_to_profile(github_profile, profile)
        GitProfileService.add_to_profile(bitbucket_profile, profile)

        # calculate end values
        profile["language_count"] = len(profile["languages"])
        profile["topic_count"] = len(profile["topics"])

        return profile


    @staticmethod
    def create_profile():
        profile = {}

        # set default values
        profile["follower_count"] = 0
        profile["repo_count"] = 0
        profile["original_repo_count"] = 0
        profile["forked_repo_count"] = 0
        profile["languages"] = set({})
        profile["language_count"] = 0
        profile["topics"] = set({})
        profile["topic_count"] = 0
        profile["watchers_count"] = 0

        return profile


    @staticmethod
    def add_to_profile(profile, final_profile):
        # loop through profile
        for key in profile:

            # add count value to existing count
            if type(profile[key]) is int:
                final_profile[key] += profile[key]

            # add values to existing set
            elif type(profile[key]) is set:
                for value in profile[key]:
                    final_profile[key].add(value)
