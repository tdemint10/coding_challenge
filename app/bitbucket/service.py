from app.routes import app
from app.exceptions import ForbiddenException

import requests


# Bitbucket API url and paths for the requests
BASE_URL = "https://api.bitbucket.org/2.0"

GET_REPOS_ENDPOINT = "repositories/%s?page=%d"
GET_FOLLOWERS_ENDPOINT = "teams/%s/followers"
GET_WATCHERS_ENDPOINT = "repositories/%s/%s/watchers"


class BitbucketService:
    @staticmethod
    def get_repos(team: str):
        app.logger.debug(f"BitbucketService - get_repos - team: {team}")

        repos = []
        page = 1

        # track when done looping through pages
        next_page_exists = True

        # loop through paginated responses
        while next_page_exists:
            # build url for the needed request
            request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % (team, page)
            app.logger.debug(f"request_url: {request_url}")

            # make request
            r = requests.get(request_url)

            if r.status_code == 403:
                app.logger.error("FAILED - Bitbucket Forbidden")
                raise ForbiddenException(f"FAILED - Access Forbidden to Bitbucket Team: {team}. (Bitbucket API rate limit may be exceeded)")
            elif not r.status_code == 200:
                app.logger.error(f"FAILED to get Bitbucket Repositories for: {team}")
                raise Exception(f"FAILURE - request failed - {request_url}")

            # append data
            repos.extend(r.json()["values"])
            page += 1


            if not "next" in r.json():
                next_page_exists = False

        # return result
        return repos


    @staticmethod
    def get_followers_count(team: str):
        app.logger.debug(f"BitbucketService - get_followers_count - team: {team}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_FOLLOWERS_ENDPOINT}" % team
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url)

        if r.status_code == 403:
            app.logger.error("FAILED - Bitbucket Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Bitbucket Team: {team}. (Bitbucket API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get Bitbucket Watchers for: {team}/{repo}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return follower count
        if "size" in r.json():
            return r.json()["size"]
        else:
            return len(r.json()["values"])


    @staticmethod
    def get_watchers_count(team: str, repo: str):
        app.logger.debug(f"BitbucketService - get_watchers_count - team: {team}, repo: {repo}")

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
        if "size" in r.json():
            return r.json()["size"]
        else:
            return len(r.json()["values"])


    @staticmethod
    def get_profile(team: str):
        app.logger.info(f"BitbucketService - get_bitbucket_profile - team: {team}")

        # create profile object to return
        profile = BitbucketService.create_empty_profile()

        repos = BitbucketService.get_repos(team)

        # populate profile values
        profile["repo_count"] = len(repos)
        profile["follower_count"] = BitbucketService.get_followers_count(team)

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
        profile["follower_count"] = 0
        profile["languages"] = set({})
        profile["watchers_count"] = 0

        return profile
