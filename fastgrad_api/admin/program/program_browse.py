from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("program_browse", __name__)


@blueprint.route("/browse", methods=["GET"])
async def browse_course() -> dict:
    query = "SELECT * FROM program"
    params = request.args.to_dict()
    if "q" in params:
        query += (
            f" WHERE id LIKE '%{params['q']}%' OR name_th LIKE "
            f"'%{params['q']}%' OR name_en LIKE '%{params['q']}%' "
            f" OR start_year LIKE '%{params['q']}%' OR end_year LIKE'%{params['q']}%'"
        )

    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    if result == []:
        return {"status": "error", "msg": "Not Found "}
    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "program_id": program_id,
                "start_year": start_year,
                "end_year": end_year,
                "program_name_th": program_name_th,
                "program_name_en": program_name_en,
            }
            for program_id, start_year, end_year, program_name_th, program_name_en, *_ in result
        ],
    }
