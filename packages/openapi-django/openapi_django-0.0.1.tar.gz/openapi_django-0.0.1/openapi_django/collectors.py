import os
import re

from django.urls import URLPattern
from openapi_django.objects import Route, Method


def normalize_str_route(_url_pattern: URLPattern):
    _route = _url_pattern.pattern._route
    if not _route:
        return ''
    routes = _route.split("/")

    result = []
    for _route in routes:
        re_route = re.findall(":([a-zA-Z0-9-_]+)>", _route)
        if not re_route:
            continue
        result.append(re_route[0])
    return "/".join(["{" + item + "}" for item in result])


def collect_routes(all_resolver):
    paths = []
    for resolver in all_resolver:
        if resolver.app_name == 'admin':
            continue
        pattern = resolver.pattern
        views = resolver.urlconf_name.views

        for url_pattern in resolver.urlconf_name.urlpatterns:
            route = Route(route=os.path.join(pattern._route, normalize_str_route(url_pattern)))
            view = getattr(views, url_pattern.lookup_str.split(".")[-1])
            for method_name in view.http_method_names:
                if hasattr(view, method_name):
                    try:
                        data = getattr(view, method_name)("openapi")
                    except Exception as e:
                        print(e)
                        continue
                    route.methods.append(Method.from_data(method_name=method_name, data=data))
            paths.append(route)
        return paths
