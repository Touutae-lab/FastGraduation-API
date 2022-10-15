from database import db
from flask import Blueprint
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("browse_plan", __name__)


@blueprint.route("/browse/<program_id>", methods=["GET"])
@verify_session()
def browse_category(program_id: int) -> dict:
    query = "SELECT * FROM plan WHERE program_id = %s"

    cursor = db.cursor()
    cursor.execute(query, [program_id])

    result = cursor.fetchall()
    if result == []:
        return {"status": "success", "msg": "not found"}

    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "id": id,
                "program_id": program_id,
                "name_th": name_th,
                "name_en": name_en,
                "min_credit": min_credit,
            }
            for id, program_id, name_th, name_en, min_credit, *_ in result
        ],
    }
