from app.routes import app
from app.github.service import GithubService
from app.bitbucket.service import BitbucketService


class GitProfileService:
    @staticmethod
    def get_profile(github_token: str, github_org: str, bitbucket_team: str):
        app.logger.info(f"GitProfileService - get_profile - github_org: {github_org}, bitbucket_team: {bitbucket_team}")

        # create profile object to return
        profile = GitProfileService.create_empty_profile()

        # get individual profiles from services
        github_profile = GithubService.get_profile(github_token, github_org)
        bitbucket_profile = BitbucketService.get_profile(bitbucket_team)

        # combine profiles
        GitProfileService.add_to_profile(github_profile, profile)
        GitProfileService.add_to_profile(bitbucket_profile, profile)

        # calculate values
        profile["language_count"] = len(profile["languages"])
        profile["topic_count"] = len(profile["topics"])

        return profile


    @staticmethod
    def create_empty_profile():
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
    def add_to_profile(module_profile, git_profile):
        # loop through profile
        for key in module_profile:

            # add count value to existing count
            if type(module_profile[key]) is int:
                git_profile[key] += module_profile[key]

            # add values to existing set
            elif type(module_profile[key]) is set:
                for value in module_profile[key]:
                    git_profile[key].add(value)
