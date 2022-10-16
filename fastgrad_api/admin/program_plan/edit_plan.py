from typing import Any, Dict, Final, FrozenSet

from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("edit_plan", __name__)

PLAN_COLS: Final[FrozenSet[str]] = frozenset(
    {
        "min_credit",
        "program_id",
        "name_en",
        "name_th",
    }
)


@blueprint.route("/edit/<plan_id>", methods=["GET", "POST"])
@verify_session()
def plan_edit(plan_id: int) -> dict:
    """
    request API spec
    {
        "min_credit": int,
        "program_id": int,
        "name_en": str,
        "name_th": str,
        "default_course_plan": ["001101", "001102", ...]
    }
    """

    if request.method == "GET":
        query: str = "SELECT * FROM `plan` WHERE `id` = %(plan_id)s"
        vals: Dict[str, Any] = {"plan_id": plan_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        field_names = [i[0] for i in mycursor.description]
        qplan_res = mycursor.fetchall()

        if not qplan_res:
            return {
                "status": "failed",
                "msg": f"The program plan with ID {plan_id} is not in the database",
            }

        query: str = (
            "SELECT * FROM `default_course_plan` WHERE `plan_id` = %(plan_id)s"
        )
        vals: Dict[str, Any] = {"plan_id": plan_id}

        mycursor.execute(query, vals)
        qcourse_res = mycursor.fetchall()

        query: str = (
            "SELECT * FROM `plan_requirement` WHERE `plan_id` = %(plan_id)s"
        )
        vals: Dict[str, Any] = {"plan_id": plan_id}

        mycursor.execute(query, vals)
        qrequired_res = mycursor.fetchall()

        result = {
            field: row[i]
            for i, field in enumerate(field_names)
            for row in qplan_res
        }
        result["default_course_plan"] = [
            "%06d" % row[0] for row in qcourse_res
        ]
        result["plan_requirement"] = [
            {"category_id": cat_id, "min_credit": min_credit}
            for *_, cat_id, min_credit in qrequired_res
        ]

        return {"status": "success", "msg": "OK", "data": result}

    if request.method == "POST":
        # check if plan_id exists in plan
        query: str = "SELECT COUNT(*) FROM `plan` WHERE `id` = %(plan_id)s"
        vals: Dict[str, Any] = {"plan_id": plan_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        qexists = mycursor.fetchall()

        if qexists[0] == 0:
            return {
                "status": "failed",
                "msg": f"The program plan with ID {plan_id} is not in the database",
            }

        # check if user provides all required fields
        data = request.get_json()
        if not isinstance(data, dict):
            return {
                "status": "failed",
                "msg": "The request data must be JSON Object",
            }

        if not PLAN_COLS.issubset(data.keys()):
            return {"status": "failed", "msg": "Not enough key to update"}

        # update the plan
        query: str = (
            "UPDATE `plan` SET "
            + ", ".join(f"`{col}` = %({col})s" for col in PLAN_COLS)
            + " WHERE `id` = %(plan_id)s"
        )
        vals: Dict[str, Any] = {field: data.get(field) for field in PLAN_COLS}
        vals["plan_id"] = plan_id

        mycursor.execute(query, vals)
        db.commit()

        # if default_course_plan is provided, update that as well
        if "default_course_plan" in data:
            courses = data.get("default_course_plan")

            query: str = "DELETE FROM `default_course_plan` WHERE `plan_id` = %(plan_id)s"
            vals: Dict[str, Any] = {"plan_id": plan_id}
            mycursor.execute(query, vals)
            db.commit()

            query: str = (
                "INSERT INTO `default_course_plan` (`course_id`, `plan_id`) VALUES "
                + ", ".join(["(%s, %s)"] * len(courses))
            )
            vals = []
            for course in courses:
                vals.append(course)
                vals.append(plan_id)

            mycursor.execute(query, vals)
            db.commit()

        return {"status": "success", "msg": "OK"}
