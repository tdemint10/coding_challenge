BASE_ROUTE = "github"


def register_routes(api, app):
    from .controller import api as github_api

    api.add_namespace(github_api, path=f"/{BASE_ROUTE}")
