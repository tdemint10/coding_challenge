from app.routes import app
from app.exceptions import ForbiddenException

import requests


# GitHub API url and paths for the requests
BASE_URL = "https://api.github.com"

GET_REPOS_ENDPOINT = "users/%s/repos"
GET_FOLLOWERS_ENDPOINT = "users/%s/followers"
GET_LANGUAGES_ENDPOINT = "repos/%s/%s/languages"
GET_TOPICS_ENDPOINT = "repos/%s/%s/topics"


class GithubService:
    @staticmethod
    def get_repos(token: str, organization: str):
        app.logger.debug(f"GithubService - get_repos - organization: {organization}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % organization
        app.logger.debug(f"request_url: {request_url}")

        # make request
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"
        r = requests.get(request_url, headers=headers)

        # handle bad response
        if r.status_code == 403:
            app.logger.error("FAILED - GitHub Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Github Organization: {organization}. (GitHub API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Repositories for: {organization}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return data
        return r.json()


    @staticmethod
    def get_followers(token: str, organization: str):
        app.logger.debug(f"GithubService - get_followers - organization: {organization}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_FOLLOWERS_ENDPOINT}" % organization
        app.logger.debug(f"request_url: {request_url}")

        # make request
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"
        r = requests.get(request_url, headers=headers)

        # handle bad response
        if r.status_code == 403:
            app.logger.error("FAILED - GitHub Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Github Organization: {organization}. (GitHub API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Followers for: {organization}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return data
        return r.json()


    @staticmethod
    def get_languages(token: str, organization: str, repo: str):
        app.logger.debug(f"GithubService - get_languages - organization: {organization}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_LANGUAGES_ENDPOINT}" % (organization, repo)
        app.logger.debug(f"request_url: {request_url}")

        # make request
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"
        r = requests.get(request_url, headers=headers)

        # handle bad response
        if r.status_code == 403:
            app.logger.error("FAILED - GitHub Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Github Organization: {organization}. (GitHub API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Languages for: {organization}/{repo}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return data
        return r.json()


    @staticmethod
    def get_topics(token: str, organization: str, repo: str):
        app.logger.debug(f"GithubService - get_topics - organization: {organization}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_TOPICS_ENDPOINT}" % (organization, repo)
        app.logger.debug(f"request_url: {request_url}")

        # make request
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        r = requests.get(request_url, headers=headers)

        # handle bad response
        if r.status_code == 403:
            app.logger.error("FAILED - GitHub Forbidden")
            raise ForbiddenException(f"FAILED - Access Forbidden to Github Organization: {organization}. (GitHub API rate limit may be exceeded)")
        elif not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Topics for: {organization}/{repo}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        # return data
        return r.json()["names"]


    @staticmethod
    def get_profile(token: str, organization: str):
        app.logger.info(f"GithubService - get_github_profile - organization: {organization}")

        # create profile object to return
        profile = GithubService.create_empty_profile()

        # populate profile values
        profile["follower_count"] = len(GithubService.get_followers(token, organization))
        repos = GithubService.get_repos(token, organization)

        # update values for each individual repo
        profile["repo_count"] = len(repos)
        for repo in repos:
            if repo["fork"]:
                profile["forked_repo_count"] += 1
            else:
                profile["original_repo_count"] += 1

            [profile["languages"].add(value.lower()) for value in GithubService.get_languages(token, organization, repo["name"])]
            [profile["topics"].add(value.lower()) for value in GithubService.get_topics(token, organization, repo["name"])]

            profile["watchers_count"] += repo["watchers_count"]

        app.logger.debug(f"GithubService - profile - {profile}")

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
        profile["topics"] = set({})
        profile["watchers_count"] = 0

        return profile
