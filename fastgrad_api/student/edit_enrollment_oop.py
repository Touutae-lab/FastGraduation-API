from typing import Dict, Final, FrozenSet, List

from database import db_oop as db
from flask import Blueprint, g, request
from mysql.connector.optionfiles import re
from route import Route, register_route
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("edit_enrollment_oop", __name__)

_COURSE_COLS: Final[FrozenSet[str]] = frozenset(
    {
        "course_id",
        "cat_id",
        "term",
        "year",
        "grade",
    }
)

_GRADE: Dict[str, float] = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0,
}


class UpdateEnrollment(Route):
    def __init__(self) -> None:
        super().__init__(path="/edit_enrollment_oop", methods=["GET", "POST"])

    @verify_session()
    def get(self, *args, **kwargs) -> dict:
        session: SessionContainer = g.supertokens
        user_id = session.get_user_id()
        cursor = db.execute(
            "SELECT student_id FROM student WHERE user_id = %s", [user_id]
        )
        stu_id = cursor.fetchall()[0][0]

        query = "SELECT * FROM enrollment WHERE student_id = %s"
        cursor, _ = db.execute(query, [stu_id])
        cols = [i[0] for i in cursor.description]
        result = cursor.fetchall()

        return {
            "status": "success",
            "msg": "OK",
            "data": [
                {col: row[i] for i, col in enumerate(cols)} for row in result
            ],
        }

    @verify_session()
    def post(self, *args, **kwargs) -> dict:
        session: SessionContainer = g.supertokens
        user_id = session.get_user_id()
        cursor = db.execute(
            "SELECT student_id FROM student WHERE user_id = %s", [user_id]
        )
        stu_id = cursor.fetchall()[0][0]

        if stu_id is None or not re.fullmatch("^[0-9]{9}$", str(stu_id)):
            return {
                "status": "failed",
                "msg": "Cannot recognize the current student number.",
            }

        data = request.get_json()

        if data is None:
            return {"status": "failed", "msg": "data cannot be null"}

        query = "DELETE FROM enrollment WHERE student_id = %s"
        cursor.execute(query, [stu_id])

        if len(data) == 0:
            return {
                "status": "success",
                "msg": "OK; no student enrollments of "
                + stu_id
                + " are in the database now.",
            }

        query = (
            "INSERT INTO enrollment (student_id, course_id, category_id, term, year, grade, grade_no) VALUES "
            + ", ".join(["(%s, %s, %s, %s, %s, %s, %s)"] * len(data))
        )
        records: List[tuple] = []

        for record in data:
            records.extend(
                (
                    stu_id,
                    record["course_id"],
                    record["cat_id"],
                    record["term"],
                    record["year"],
                    record["grade"],
                    _GRADE.get(record["grade"], 0),
                )
            )

        cursor.execute(query, records)
        db.commit()

        return {
            "status": "success",
            "msg": f"OK; {len(data)} student enrollment(s) of {stu_id} have been updated.",
        }


register_route(blueprint, UpdateEnrollment())
