from typing import Any, Dict, Final, FrozenSet

from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_category_edit", __name__)

CAT_COLS: Final[FrozenSet[str]] = frozenset(
    {
        "name_en",
        "name_th",
        "abbr_en",
        "abbr_th",
    }
)


@blueprint.route("/edit/<cat_id>", methods=["GET", "POST"])
@verify_session()
def cat_edit(cat_id: int) -> dict:
    """
    request API spec
    {
        "name_en": str,
        "name_th": str,
        "abbr_th": str,
        "abbr_en": str,
        "default_course_category": ["001101", ...],
    }
    """

    if request.method == "GET":
        query: str = "SELECT * FROM `course_category` WHERE `id` = %(cat_id)s"
        vals: Dict[str, Any] = {"cat_id": cat_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        field_names = [i[0] for i in mycursor.description]
        qcat_res = mycursor.fetchall()

        if not qcat_res:
            return {
                "status": "failed",
                "msg": f"The course category with ID {cat_id} is not in the database",
            }

        query: str = "SELECT * FROM `default_course_category` WHERE `category_id` = %(cat_id)s"
        vals: Dict[str, Any] = {"cat_id": cat_id}

        mycursor.execute(query, vals)
        qcourse_res = mycursor.fetchall()

        result = {
            field: row[i]
            for i, field in enumerate(field_names)
            for row in qcat_res
        }
        result["default_course_category"] = [row[0] for row in qcourse_res]

        return {"status": "success", "msg": "OK", "data": result}

    if request.method == "POST":
        # check if cat_id exists in category
        query: str = (
            "SELECT COUNT(*) FROM `course_category` WHERE `id` = %(cat_id)s"
        )
        vals: Dict[str, Any] = {"cat_id": cat_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        qexists = mycursor.fetchall()

        if qexists[0] == 0:
            return {
                "status": "failed",
                "msg": f"The course category with ID {cat_id} is not in the database",
            }

        # check if user provides all required fields
        data = request.get_json()
        if not isinstance(data, dict):
            return {
                "status": "failed",
                "msg": "The request data must be JSON Object",
            }

        if not CAT_COLS.issubset(data.keys()):
            return {"status": "failed", "msg": "Not enough key to update"}

        # update the plan
        query: str = (
            "UPDATE `course_category` SET "
            + ", ".join(f"`{col}` = %({col})s" for col in CAT_COLS)
            + " WHERE `id` = %(cat_id)s"
        )
        vals: Dict[str, Any] = {field: data.get(field) for field in CAT_COLS}
        vals["cat_id"] = cat_id

        mycursor.execute(query, vals)
        db.commit()

        # if default_course_category is provided, update that as well
        if "default_course_category" in data:
            courses = data.get("default_course_category")

            query: str = "DELETE FROM `default_course_category` WHERE `category_id` = %(cat_id)s"
            vals: Dict[str, Any] = {"cat_id": cat_id}
            mycursor.execute(query, vals)
            db.commit()

            query: str = (
                "INSERT INTO `default_course_category` (`course_id`, `category_id`) VALUES "
                + ", ".join(["(%s, %s)"] * len(courses))
            )
            vals = []
            for course in courses:
                vals.append(course)
                vals.append(cat_id)

            mycursor.execute(query, vals)
            db.commit()

        return {"status": "success", "msg": "OK"}
