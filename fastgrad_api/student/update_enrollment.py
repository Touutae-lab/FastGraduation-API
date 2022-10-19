from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("update_enrollment", __name__)

_GRADE = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0,
}


@blueprint.route("/update_enrollment", methods=["POST"])
@verify_session()
def update_enrollment() -> dict:
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
                _GRADE[record["grade"]],
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
