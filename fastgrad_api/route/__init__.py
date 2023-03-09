from collections import Iterable
from typing import Union

from flask import Blueprint

from .Route import Route


def _register_helper(blueprint: Blueprint, route: Route):
    path = route.path
    methods = route.methods
    viewfunc = route.as_view()

    if isinstance(path, str):
        path = [(path, None)]

    for p, d in path:
        kwargs = {} if d is None else {"defaults": d}
        blueprint.add_url_rule(
            p, view_func=viewfunc, methods=methods, **kwargs
        )


def register_route(blueprint: Blueprint, route: Union[Iterable[Route], Route]):
    if isinstance(route, Route):
        route = [route]
    for r in route:
        _register_helper(blueprint, r)
