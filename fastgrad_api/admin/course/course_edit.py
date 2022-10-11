# from admin.student.Utility_Function import checklanguage
from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

from ..Utility_Function import validate

blueprint: Blueprint = Blueprint("course_edit", __name__)


@blueprint.route("/edit/<course_id>", methods=["GET", "POST"])
@verify_session()
def course_edit(course_id) -> dict:
    status = "success"
    msg = "ok"
    results = []
    tag_list = [
        "course_name_th",
        "description_th",
        "course_id",
        "cousre_id_pre",
        "Term_one",
        "Term_two",
        "Term_summer",
        "pregroup_id",
        "credit",
        "course_name_en",
        "description_en",
    ]

    if request.method == "POST":
        datas = request.get_json()
        for data in datas:
            results.append(datas.get(data))
        status, msg = validate(tag_list, datas)
        if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
            return msg

        query = """UPDATE course
                    INNER JOIN prerequisite ON course.id=prerequisite.course_id
                    SET name_en=%s,name_th =%s ,credit=%s,description_th=%s
                    ,description_en=%s,term_1=%s,term_2=%s,term_s=%s,precousre_id=%s,pregroup_id=%s
                    WHERE course_id=""" + str(
            course_id
        )
        cursor = db.cursor()
        cursor.execute(query, results)
        db.commit()

    query = (
        "SELECT * FROM `course`,prerequisite WHERE  course.id=prerequisite.course_id and id="
        + course_id
    )

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()[0]
    (
        name_th,
        name_en,
        credit,
        description_th,
        description_en,
        term_1,
        term_2,
        term_s,
        course_id,
        precousre_id,
        pregroup_id,
        *_,
    ) = result
    return {
        "status": status,
        "msg": msg,
        "data": {
            "course_id": course_id,
            "course_name_th": name_th,
            "course_name_en": name_en,
            "credit": credit,
            "description_th": description_th,
            "description_en": description_en,
            "Term_one": term_1,
            "Term_two": term_2,
            "Term_summer": term_s,
            "precousre_id": precousre_id,
            "pregroup_id": pregroup_id,
        },
    }
