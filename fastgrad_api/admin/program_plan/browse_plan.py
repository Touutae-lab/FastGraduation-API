from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("browse_plan", __name__)


@blueprint.route("/plan/browse", methods=["GET"])
async def browse_category() -> dict:
    query = "SELECT * FROM plan"
    params = request.args.to_dict()

    if "q" in params:
        query += (
            f" WHERE name_th LIKE "
            f"'%{params['q']}%' OR program_id LIKE '%{params['q']}%' OR name_en LIKE '%{params['q']}%'"
        )

    cursor = db.cursor()
    cursor.execute(query)

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
                "is_for_all": is_for_all,
            }
            for id, program_id, name_th, name_en, min_credit, is_for_all, *_ in result
        ],
    }
