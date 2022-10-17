from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("plan_delete", __name__)


@blueprint.route("/delete/<plan_id>", methods=["GET"])
@verify_session()
def plan_delete(plan_id: int) -> dict:
    val = "SELECT * FROM plan WHERE id ="
    query = "DELETE FROM plan WHERE id = "
    params = request.args.to_dict()
    if "plan_id" in params:
        query += params["plan_id"]
        val += params["plan_id"]
    else:
        return {
            "status": "fail",
            "msg": " need to input plan_id not  program_id",
        }

    cursor = db.cursor()
    cursor.execute(val)
    temp = cursor.fetchall()

    cursor = db.cursor()
    cursor.execute(query)

    db.commit()
    if temp == []:
        return {"status": "fail", "msg": "not found this plan id"}

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
