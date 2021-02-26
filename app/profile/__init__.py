BASE_ROUTE = "profile"


def register_routes(api, app, root="api"):
    from .controller import api as profile_api

    api.add_namespace(profile_api, path=f"/{root}/{BASE_ROUTE}")
