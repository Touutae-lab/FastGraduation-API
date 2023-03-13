from typing import Any, Dict
from database import db
from flask import Blueprint, request
from route import Route, register_route
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_delete", __name__)


class CourseDelete(Route):
    def __init__(self) -> None:
        super().__init__(path="/delete/<course_id>", methods=["POST"])

    @verify_session()
    def post(self, *args, **kwargs):
        course_id = kwargs.get("course_id")
        query: str = "DELETE FROM `course` WHERE `id` = %(course_id)s"
        vals: Dict[str, Any] = {"course_id": course_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)
        db.commit()

        query = "SELECT id FROM course WHERE `id` = %(course_id)s"

        cursor = db.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        # Not Found
        if result == []:
            return {
                "status": "success",
                "msg": "OK",
            }
        return {"status": "error", "msg": "Not Success"}


_route: Route = CourseDelete()
register_route(blueprint, _route)
