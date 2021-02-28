BASE_ROUTE = "profile"


def register_routes(api, app):
    from .controller import api as profile_api

    api.add_namespace(profile_api, path=f"/{BASE_ROUTE}")
