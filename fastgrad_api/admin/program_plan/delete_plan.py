from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("delete_plan", __name__)


@blueprint.route("/delete/<plan_id>", methods=["GET"])
@verify_session()
def plan_delete(plan_id) -> dict:
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
            }
            for id, program_id, name_th, name_en, min_credit, *_ in temp
        ],
    }
