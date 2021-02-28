from app.routes import app
from app.exceptions import ForbiddenException

import requests


# Bitbucket API url and paths for the requests
BASE_URL = "https://api.bitbucket.org/2.0"

GET_REPOS_ENDPOINT = "repositories/%s"
GET_WATCHERS_ENDPOINT = "repositories/%s/%s/watchers"


class BitbucketService:
    @staticmethod
    def get_repos(team: str):
        app.logger.debug(f"BitbucketService - get_repos - team: {team}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % team
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url)

        if r.status_code == 403:
            app.logger.error("FAILED - Bitbucket Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Bitbucket Team: {team}. (Bitbucket API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get Bitbucket Repositories for: {team}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return data
        return r.json()["values"]


    @staticmethod
    def get_watchers_count(team: str, repo: str):
        app.logger.debug(f"BitbucketService - get_watchers - team: {team}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_WATCHERS_ENDPOINT}" % (team, repo)
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url)

        if r.status_code == 403:
            app.logger.error("FAILED - Bitbucket Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Bitbucket Team: {team}. (Bitbucket API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get Bitbucket Watchers for: {team}/{repo}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return watchers
        return r.json()["size"]


    @staticmethod
    def get_profile(team: str):
        app.logger.info(f"BitbucketService - get_bitbucket_profile - team: {team}")

        # create profile object to return
        profile = BitbucketService.create_empty_profile()

        repos = BitbucketService.get_repos(team)

        # populate profile values
        profile["repo_count"] = len(repos)

        # update values for each individual repo
        for repo in repos:
            profile["languages"].add(repo["language"].lower())

            profile["watchers_count"] += BitbucketService.get_watchers_count(team, repo["name"])

        return profile


    @staticmethod
    def create_empty_profile():
        profile = {}

        # set default values
        profile["repo_count"] = 0
        profile["languages"] = set({})
        profile["watchers_count"] = 0

        return profile
