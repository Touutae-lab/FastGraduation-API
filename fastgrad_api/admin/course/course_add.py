from typing import Any, Dict
from database import db_oop as db
from flask import Blueprint, request
from route import Route, register_route
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_add", __name__)


class CourseAdd(Route):
    def __init__(self) -> None:
        super().__init__(path="/add", methods=["POST"])

    @verify_session()
    def post(self, *args, **kwargs):
        body = request.get_json()

        db.insert("course", body)

        query = "SELECT id FROM course WHERE `id` = %(course_id)s"
        vals: Dict[str, Any] = {"course_id": body["id"]}
        cursor, _ = db.execute(query, vals)

        result = cursor.fetchall()

        # Found
        if result != []:
            return {
                "status": "success",
                "msg": "OK",
            }
        return {"status": "error", "msg": "Not Success"}


_route: Route = CourseAdd()
register_route(blueprint, _route)
