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
    def get_repos(name: str):
        app.logger.debug(f"GithubService - get_repos - name: {name}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_REPOS_ENDPOINT}" % name
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url, auth=('tdemint10', ''))

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Repositories for: {name}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_followers(name: str):
        app.logger.debug(f"GithubService - get_followers - name: {name}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_FOLLOWERS_ENDPOINT}" % name
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url, auth=('tdemint10', ''))

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Followers for: {name}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_languages(name: str, repo: str):
        app.logger.debug(f"GithubService - get_languages - name: {name}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_LANGUAGES_ENDPOINT}" % (name, repo)
        app.logger.debug(f"request_url: {request_url}")

        # make request
        r = requests.get(request_url, auth=('tdemint10', ''))

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Languages for: {name}/{repo}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_topics(name: str, repo: str):
        app.logger.debug(f"GithubService - get_topics - name: {name}, repo: {repo}")

        # build url for the needed request
        request_url = f"{BASE_URL}/{GET_TOPICS_ENDPOINT}" % (name, repo)
        app.logger.debug(f"request_url: {request_url}")

        # make request
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        r = requests.get(request_url, auth=('tdemint10', ''), headers=headers)

        if not r.status_code == 200:
            app.logger.error(f"FAILED to get GitHub Topics for: {name}/{repo}")
            return []

        # return data
        return r.json()


    @staticmethod
    def get_github_profile(name: str):
        app.logger.info(f"GithubService - get_github_profile - name: {name}")

        followers = GithubService.get_followers(name)
        repos = GithubService.get_repos(name)

        languages = []
        topics = []
        watchers_count = 0

        original_repo_count = 0
        forked_repo_count = 0
        for repo in repos:
            if repo["fork"]:
                original_repo_count += 1
            else:
                forked_repo_count += 1

            repo_languages = GithubService.get_languages(name, repo["name"])
            for language in repo_languages:
                if not language in languages:
                    languages.append(language)

            repo_topics = GithubService.get_topics(name, repo["name"])
            for topic in repo_topics:
                if not topic in topics:
                    topics.append(topic)

            watchers_count += repo["watchers_count"]

        profile = {
            "user": name,
            "follower_count": len(followers),
            "repo_count": len(repos),
            "original_repo_count": original_repo_count,
            "forked_repo_count": forked_repo_count,
            "languages": languages,
            "language_count": len(languages),
            "topics": topics,
            "topic_count": len(topics),
            "watchers_count": watcher_count
        }

        return profile
