from typing import Any, Dict, Final, FrozenSet

from database import db
from flask import Blueprint, request
from route import Route, register_route
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_edit", __name__)

COURSE_COLS: Final[FrozenSet[str]] = frozenset(
    {
        "id",
        "name_th",
        "name_en",
        "credit",
        "description_th",
        "description_en",
        "term_1",
        "term_2",
        "term_s",
        "min_year",
        "consent_dept",
    }
)

"""
request API spec
{
    "id": str,
    "name_th": str,
    "name_en": str,
    "credit": str,
    "description_th": str,
    "description_en": str,
    "term_1": str,
    "term_2": str,
    "term_s": str,
    "min_year": str,
    "consent_dept": str,
}
"""


class CourseEdit(Route):
    def __init__(self) -> None:
        super().__init__(path="/edit/<course_id>", methods=["GET", "POST"])

    @verify_session()
    def get(self, *args, **kwargs):
        course_id = kwargs.get("course_id")
        query: str = "SELECT * FROM `course` WHERE `id` = %(course_id)s"
        vals: Dict[str, Any] = {"course_id": course_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        field_names = [i[0] for i in mycursor.description]
        qcat_res = mycursor.fetchall()

        if not qcat_res:
            return {
                "status": "failed",
                "msg": f"The course with ID {course_id} is not in the database",
            }

        result = {
            field: row[i]
            for i, field in enumerate(field_names)
            for row in qcat_res
        }

        return {"status": "success", "msg": "OK", "data": result}

    @verify_session()
    def post(self, *args, **kwargs):
        course_id = kwargs.get("course_id")
        # check if course_id exists in category
        query: str = "SELECT COUNT(*) FROM `course` WHERE `id` = %(course_id)s"
        vals: Dict[str, Any] = {"course_id": course_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        qexists = mycursor.fetchall()

        if qexists[0] == 0:
            return {
                "status": "failed",
                "msg": f"The course category with ID {course_id} is not in the database",
            }

        # check if user provides all required fields
        data = request.get_json()
        if not isinstance(data, dict):
            return {
                "status": "failed",
                "msg": "The request data must be JSON Object",
            }

        if not COURSE_COLS.issubset(data.keys()):
            return {"status": "failed", "msg": "Not enough key to update"}

        # update the plan
        query: str = (
            "UPDATE `course` SET "
            + ", ".join(f"`{col}` = %({col})s" for col in COURSE_COLS)
            + " WHERE `id` = %(course_id)s"
        )
        vals: Dict[str, Any] = {
            field: data.get(field) for field in COURSE_COLS
        }
        vals["course_id"] = course_id

        mycursor.execute(query, vals)
        db.commit()

        return {
            "status": "success",
            "msg": "OK",
        }


_route = CourseEdit()
register_route(blueprint, _route)
