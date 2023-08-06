from openapi_django.collectors import collect_routes
from openapi_django.objects import OpenAPI


def generate(root_urlconf):
    root_urlconf = __import__(root_urlconf)
    openapi = OpenAPI()
    openapi.routes = collect_routes(all_resolver=root_urlconf.urls.urlpatterns)
    return openapi.json()
