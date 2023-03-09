from flask import Blueprint, request
from route import Route, register_route

blueprint: Blueprint = Blueprint("test_new_route", __name__)


class TestController(Route):
    def __init__(
        self,
        path=[
            ("/test_new_route/<path_msg>", None),
            ("/test_new_route", {"path_msg": None}),
        ],
        methods=["GET", "POST"],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(path=path, methods=methods, *args, **kwargs)

    def get(self, *args, **kwargs):
        pathmsg = kwargs.get("path_msg", "<none>")
        return {
            "status": "success",
            "data": {
                "postmsg": "<none> because it is GET method.",
                "pathmsg": pathmsg,
            },
        }

    def post(self, *args, **kwargs):
        postdata = request.get_json()
        postmsg = postdata.get("post_msg", "<none>")
        pathmsg = kwargs.get("path_msg", "<none>")

        return {
            "status": "success",
            "data": {
                "postmsg": postmsg,
                "pathmsg": pathmsg,
            },
        }


_route: Route = TestController()

register_route(blueprint, _route)
