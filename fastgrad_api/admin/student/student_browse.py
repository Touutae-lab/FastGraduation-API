from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("student_browse", __name__)


@blueprint.route("/browse", methods=["GET"])
async def student_browse() -> dict:
    query = "SELECT student_id,fname_en,mname_en,lname_en,fname_th,mname_th,lname_th,email,academic_year FROM user ,student WHERE  user.user_id=student.user_id"
    params = request.args.to_dict()
    if "q" in params:
        query += (
            f" AND( student_id LIKE '%{params['q']}%' OR fname_th LIKE "
            f"'%{params['q']}%' OR mname_th LIKE '%{params['q']}%'"
            f"OR lname_th LIKE '%{params['q']}%' OR fname_en LIKE '%{params['q']}%'"
            f"OR mname_en LIKE '%{params['q']}%' OR lname_en LIKE '%{params['q']}%')"
        )

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "student_id": student_id,
                "first_name_en": fname_en,
                "mid_name_en": mname_en,
                "last_name_en": lname_en,
                "first_name_th": fname_th,
                "mid_name_th": mname_th,
                "last_name_th": lname_th,
                "email": email,
            }
            for student_id, fname_en, mname_en, lname_en, fname_th, mname_th, lname_th, email, *_ in result
        ],
    }
