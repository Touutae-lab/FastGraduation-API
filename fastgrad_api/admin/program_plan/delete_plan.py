from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("delete_plan", __name__)


@blueprint.route("/plan/delete/<plan_id>", methods=["GET"])
async def plan_delete(plan_id) -> dict:
    val = "SELECT * FROM plan WHERE id ="
    query = "DELETE FROM plan WHERE id = "
    params = request.args.to_dict()
    if "q" in params:
        query += params["q"]
        val += params["q"]

    cursor = db.cursor()
    cursor.execute(val)
    temp = cursor.fetchall()

    cursor = db.cursor()
    cursor.execute(query)

    db.commit()

    return {
        "status": "success",
        "msg": "record have been deleted.",
        "this reccord": [
            {
                "id": id,
                "program_id": program_id,
                "name_th": name_th,
                "name_en": name_en,
                "min_credit": min_credit,
                "is_for_all": is_for_all,
            }
            for id, program_id, name_th, name_en, min_credit, is_for_all, *_ in temp
        ],
    }
