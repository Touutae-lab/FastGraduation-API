from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("browse_course", __name__)


@blueprint.route("/browse_course", methods=["GET"])
@verify_session()
def browse_course() -> dict:
    query = (
        "SELECT id, name_th, name_en, category_id "
        "FROM course "
        "JOIN default_course_plan ON id = default_course_plan.course_id "
        "LEFT JOIN default_course_category ON id = default_course_category.course_id "
        "WHERE plan_id = 1 AND "
        '      (id LIKE "%%%(kw)s%%" OR '
        '       name_en LIKE "%%%(kw)s%%" OR '
        '       name_th LIKE "%%%(kw)s%%")'
    )
    params = request.args.to_dict()
    kw = ""
    if "q" in params:
        kw = params["q"]

    cursor = db.cursor()
    cursor.execute(query % {"kw": kw})

    result = cursor.fetchall()

    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "course_id": f"{course_id:06d}",
                "course_name_th": course_name_th,
                "course_name_en": course_name_en,
                "cat_id": cat_id,
            }
            for course_id, course_name_th, course_name_en, cat_id, *_ in result
        ],
    }
