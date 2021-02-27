from app.routes import app

import requests


# Bitbucket API url and paths for the requests
BASE_URL = "https://api.bitbucket.org/2.0"

GET_REPOS_ENDPOINT = "repositories/%s"
GET_WATCHERS_ENDPOINT = "repositories/%s/%s/watchers"


class BitbucketService:
    @staticmethod
    def get_repos(name: str):
        app.logger.debug(f"BitbucketService - get_repos - name: {name}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % name
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            r = requests.get(request_url)
        except:
            app.logger.error(f"FAILURE - request failed - {request_url}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get Bitbucket Repositories for: {name}")
            return []

        # return data
        return r.json()["values"]


    @staticmethod
    def get_watchers_count(name: str, repo: str):
        app.logger.debug(f"BitbucketService - get_watchers - name: {name}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_WATCHERS_ENDPOINT}" % (name, repo)
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            r = requests.get(request_url)
        except:
            app.logger.error(f"FAILURE - request failed - {request_url}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get Bitbucket Watchers for: {name}/{repo}")
            return 0

        # return watchers
        return r.json()["size"]


    @staticmethod
    def get_profile(name: str):
        app.logger.info(f"BitbucketService - get_bitbucket_profile - name: {name}")

        repos = BitbucketService.get_repos(name)

        languages = set({})
        watchers_count = 0

        for repo in repos:
            # add language if needed (always lowercase)
            languages.add(repo["language"].lower())

            watchers_count += BitbucketService.get_watchers_count(name, repo["name"])

        profile = {
            "repo_count": len(repos),
            "languages": languages,
            "watchers_count": watchers_count
        }

        return profile
