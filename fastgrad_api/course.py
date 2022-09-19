from database import db
from flask import Blueprint, request

test_blueprint: Blueprint = Blueprint("test_blueprint", __name__)


@test_blueprint.route("/api/student/browse_course", methods=["GET"])
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


GRADE = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0,
}


@test_blueprint.route("/api/student/update_enrollment", methods=["POST"])
async def update_enrollment() -> dict:
    data = request.get_json()
    query = "INSERT INTO enrollment (student_id, course_id, category_id, term, year, grade, grade_no) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    records = []
    for record in data:
        records.append(
            (
                "640510112",
                record["course_id"],
                record["cat_id"],
                record["term"],
                record["year"],
                record["grade"],
                GRADE[record["grade"]],
            )
        )
    result = []

    cursor = db.cursor()
    for record in records:
        exec_result = cursor.execute(query, record)
        result.append(exec_result)

    db.commit()

    return {
        "status": "success",
        "msg": "All have been added for student 640510112.",
        "data": result,
    }

    return {
        "status": "failure",
        "msg": "We encountered a problem while adding enrolled course for student 640510112.",
    }
