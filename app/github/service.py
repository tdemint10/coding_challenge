from app.routes import app

import requests


# GitHub API url and paths for the requests
BASE_URL = "https://api.github.com"

GET_REPOS_ENDPOINT = "users/%s/repos"
GET_FOLLOWERS_ENDPOINT = "users/%s/followers"
GET_LANGUAGES_ENDPOINT = "repos/%s/%s/languages"
GET_TOPICS_ENDPOINT = "repos/%s/%s/topics"


class GithubService:
    @staticmethod
    def get_repos(token: str, name: str):
        app.logger.debug(f"GithubService - get_repos - name: {name}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % name
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            headers = {}
            if token:
                headers["Authorization"] = f"token {token}"
            r = requests.get(request_url, headers=headers)
        except Exception as err:
            app.logger.error(f"FAILURE - request failed - {request_url} - {err}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Repositories for: {name}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_followers(token: str, name: str):
        app.logger.debug(f"GithubService - get_followers - name: {name}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_FOLLOWERS_ENDPOINT}" % name
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            headers = {}
            if token:
                headers["Authorization"] = f"token {token}"
            r = requests.get(request_url, headers=headers)
        except Exception as err:
            app.logger.error(f"FAILURE - request failed - {request_url} - {err}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Followers for: {name}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_languages(token: str, name: str, repo: str):
        app.logger.debug(f"GithubService - get_languages - name: {name}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_LANGUAGES_ENDPOINT}" % (name, repo)
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            headers = {}
            if token:
                headers["Authorization"] = f"token {token}"
            r = requests.get(request_url, headers=headers)
        except Exception as err:
            app.logger.error(f"FAILURE - request failed - {request_url} - {err}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Languages for: {name}/{repo}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_topics(token: str, name: str, repo: str):
        app.logger.debug(f"GithubService - get_topics - name: {name}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_TOPICS_ENDPOINT}" % (name, repo)
        app.logger.debug(f"request_url: {request_url}")

        try:
            # make request
            headers = {"Accept": "application/vnd.github.mercy-preview+json"}
            if token:
                headers["Authorization"] = f"token {token}"
            r = requests.get(request_url, headers=headers)
        except:
            app.logger.error(f"FAILURE - request failed - {request_url}")
            raise Exception(f"FAILURE - request failed - {request_url}")

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Topics for: {name}/{repo}")
            return []

        # return data
        return r.json()["names"]


    @staticmethod
    def get_profile(token: str, name: str):
        app.logger.info(f"GithubService - get_github_profile - name: {name}")

        followers = GithubService.get_followers(token, name)
        repos = GithubService.get_repos(token, name)

        languages = set({})
        topics = set({})
        watchers_count = 0

        original_repo_count = 0
        forked_repo_count = 0
        for repo in repos:
            if repo["fork"]:
                original_repo_count += 1
            else:
                forked_repo_count += 1

            # add language if needed (always lowercase)
            repo_languages = GithubService.get_languages(token, name, repo["name"])
            for language in repo_languages:
                languages.add(language.lower())

            repo_topics = GithubService.get_topics(token, name, repo["name"])
            for topic in repo_topics:
                topics.add(topic.lower())

            watchers_count += repo["watchers_count"]

        profile = {
            "follower_count": len(followers),
            "repo_count": len(repos),
            "original_repo_count": original_repo_count,
            "forked_repo_count": forked_repo_count,
            "languages": languages,
            "topics": topics,
            "watchers_count": watchers_count
        }

        return profile
