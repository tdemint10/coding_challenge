BASE_ROUTE = "bitbucket"


def register_routes(api, app, root="api"):
    from .controller import api as bitbucket_api

    api.add_namespace(bitbucket_api, path=f"/{root}/{BASE_ROUTE}")
