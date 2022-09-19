from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("browse_course", __name__)


@blueprint.route("/browse_course", methods=["GET"])
async def browse_course() -> dict:
    query = "SELECT * FROM course"
    params = request.args.to_dict()
    if "q" in params:
        query += (
            f" WHERE id LIKE '%{params['q']}%' OR name_th LIKE "
            f"'%{params['q']}%' OR name_en LIKE '%{params['q']}%'"
        )

    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "course_id": f"{course_id:06d}",
                "course_name_th": course_name_th,
                "course_name_en": course_name_en,
            }
            for course_id, course_name_th, course_name_en, *_ in result
        ],
    }
