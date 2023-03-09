from abc import ABC, abstractmethod
from typing import Dict, List, Literal, Tuple, Union

from flask import request
from supertokens_python.recipe.session.framework.flask import verify_session


class Route(ABC):
    def __init__(self, path, methods=["GET"]) -> None:
        super().__init__()
        self._methods: List[Union[Literal["GET"], Literal["POST"], Literal["DELETE"], Literal["PUT"]]] = methods
        self._path: Union[
            str, List[Tuple[str, Dict[str, Union[str, None]]]]
        ] = path

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
    
    def delete(self, *args, **kwargs):
        pass
    
    def put(self, *args, **kwargs):
        pass
    
    def as_view(self):
        def view_func(*args, **kwargs):
            if request.method == "GET":
                return self.get(*args, **kwargs)
            elif request.method == "POST":
                return self.post(*args, **kwargs)
            elif request.method == "DELETE":
                return self.delete(*args, **kwargs)
            elif request.method == "PUT":
                return self.put(*args, **kwargs)
        return view_func

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value

    @property
    def methods(self):
        return self._methods

    @methods.setter
    def methods(self, value: List[Union[Literal["GET"], Literal["POST"]]]):
        self._methods = value

    @property
    def defaults(self):
        return self._defaults

    @defaults.setter
    def defaults(self, value: Union[Dict[str, Union[str, None]], None]):
        self._defaults = value


class VerifyMixin:
    def get_verify_viewfunc(self):
        @verify_session
        def view_func():
            return self.get_viewfunc()
