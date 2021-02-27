from app.routes import app
from app.github.service import GithubService
from app.bitbucket.service import BitbucketService


class GitProfileService:
    @staticmethod
    def get_profile(github_user: str, bitbucket_user: str):
        app.logger.info(f"GitProfileService - get_profile - github_user: {github_user}, bitbucket_user: {bitbucket_user}")

        # create profile object to return
        profile = {}
        profile["github_username"] = github_user
        profile["bitbucket_username"] = bitbucket_user

        # set default values
        profile["follower_count"] = 0
        profile["repo_count"] = 0
        profile["original_repo_count"] = 0
        profile["forked_repo_count"] = 0
        profile["languages"] = []
        profile["language_count"] = 0
        profile["topics"] = []
        profile["topic_count"] = 0
        profile["watchers_count"] = 0

        github_profile = GithubService.get_profile(github_user)

        profile["repo_count"] += github_profile["repo_count"]
        profile["original_repo_count"] += github_profile["original_repo_count"]
        profile["forked_repo_count"] += github_profile["forked_repo_count"]
        profile["languages"] = github_profile["languages"]
        profile["topics"] = github_profile["topics"]
        profile["watchers_count"] = github_profile["watchers_count"]

        bitbucket_profile = BitbucketService.get_profile(bitbucket_user)

        profile["repo_count"] += bitbucket_profile["repo_count"]
        profile["watchers_count"] = bitbucket_profile["watchers_count"]

        for language in bitbucket_profile["languages"]:
            if not language in profile["languages"]:
                profile["languages"].append(language)

        profile["language_count"] = len(profile["languages"])
        profile["topic_count"] = len(profile["topics"])

        return profile
