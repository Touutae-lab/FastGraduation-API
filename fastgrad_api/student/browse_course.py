from database import db
from flask import Blueprint, g, request
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("browse_course", __name__)


@blueprint.route("/browse_course", methods=["GET"])
@verify_session()
def browse_course() -> dict:
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()
    cursor = db.cursor()

    query = "SELECT academic_year FROM student WHERE user_id = %s"
    cursor.execute(query, [user_id])
    stu_year = cursor.fetchall()[0][0]

    plan_id = 3
    if stu_year == 2020:
        plan_id = 1

    query = (
        "SELECT id, name_th, name_en, category_id "
        "FROM course "
        "JOIN default_course_plan ON id = default_course_plan.course_id "
        "LEFT JOIN default_course_category ON id = default_course_category.course_id "
        "WHERE plan_id = %(plan_id)s AND "
        '      (id LIKE "%%%(kw)s%%" OR '
        '       name_en LIKE "%%%(kw)s%%" OR '
        '       name_th LIKE "%%%(kw)s%%")'
    )
    params = request.args.to_dict()
    kw = ""
    if "q" in params:
        kw = params["q"]

    cursor.execute(query % {"kw": kw, "plan_id": plan_id})

    res_courses = cursor.fetchall()

    query = "SELECT id, abbr_th, abbr_en FROM course_category"
    cursor.execute(query)
    res_cat = cursor.fetchall()

    return {
        "status": "success",
        "msg": "OK",
        "data": {
            "available_courses": [
                {
                    "course_id": f"{course_id:06d}",
                    "course_name_th": course_name_th,
                    "course_name_en": course_name_en,
                    "cat_id": cat_id,
                }
                for course_id, course_name_th, course_name_en, cat_id, *_ in res_courses
            ],
            "categories": [
                {
                    "category_id": cat_id,
                    "abbr_th": abbr_th,
                    "abbr_en": abbr_en,
                }
                for cat_id, abbr_th, abbr_en, *_ in res_cat
            ],
        },
    }
