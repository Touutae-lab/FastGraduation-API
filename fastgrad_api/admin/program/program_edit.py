from typing import Any, Dict, Final, FrozenSet

from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("edit_program", __name__)

PROGRAM_COLS: Final[FrozenSet[str]] = frozenset(
    {
        "start_year",
        "end_year",
        "name_th",
        "name_en",
    }
)


@blueprint.route("/edit/<program_id>", methods=["GET", "POST"])
@verify_session()
def program_edit(program_id: int) -> dict:
    """
    request API spec
    {
        "start_year": int,
        "end_year": int,
        "name_th": str,
        "name_en": str,
    }
    """

    if request.method == "GET":
        query: str = "SELECT * FROM `program` WHERE `id` = %(program_id)s"
        vals: Dict[str, Any] = {"program_id": program_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        field_names = [i[0] for i in mycursor.description]
        qprogram_res = mycursor.fetchall()

        if not qprogram_res:
            return {
                "status": "failed",
                "msg": f"The program plan with ID {program_id} is not in the database",
            }

        query: str = "SELECT * FROM `plan` WHERE `program_id` = %(program_id)s"
        vals: Dict[str, Any] = {"program_id": program_id}

        mycursor.execute(query, vals)
        qplan_res = mycursor.fetchall()

        result = {
            field: row[i]
            for i, field in enumerate(field_names)
            for row in qprogram_res
        }
        result["plan_id"] = [row[0] for row in qplan_res]

        return {"status": "success", "msg": "OK", "data": result}

    if request.method == "POST":
        # check if program_id exists in program
        query: str = (
            "SELECT COUNT(*) FROM `program` WHERE `id` = %(program_id)s"
        )
        vals: Dict[str, Any] = {"program_id": program_id}

        mycursor = db.cursor()
        mycursor.execute(query, vals)

        qexists = mycursor.fetchall()

        if qexists[0] == 0:
            return {
                "status": "failed",
                "msg": f"The program with ID {program_id} is not in the database",
            }

        # check if user provides all required fields
        data = request.get_json()
        if not isinstance(data, dict):
            return {
                "status": "failed",
                "msg": "The request data must be JSON Object",
            }

        if not PROGRAM_COLS.issubset(data.keys()):
            return {"status": "failed", "msg": "Not enough key to update"}

        # update the plan
        query: str = (
            "UPDATE `program` SET "
            + ", ".join(f"`{col}` = %({col})s" for col in PROGRAM_COLS)
            + " WHERE `id` = %(program_id)s"
        )
        vals: Dict[str, Any] = {
            field: data.get(field) for field in PROGRAM_COLS
        }
        vals["program_id"] = program_id

        mycursor.execute(query, vals)
        db.commit()

        return {"status": "success", "msg": "OK"}
