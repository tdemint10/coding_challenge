BASE_ROUTE = "github"


def register_routes(api, app, root="api"):
    from .controller import api as github_api

    api.add_namespace(github_api, path=f"/{root}/{BASE_ROUTE}")
