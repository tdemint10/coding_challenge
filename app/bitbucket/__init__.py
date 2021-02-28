BASE_ROUTE = "bitbucket"


def register_routes(api, app):
    from .controller import api as bitbucket_api

    api.add_namespace(bitbucket_api, path=f"/{BASE_ROUTE}")
