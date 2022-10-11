from database import db
from flask import Blueprint, request
from supertokens_python.recipe.emailpassword.syncio import (
    get_user_by_email,
    sign_up,
)
from supertokens_python.recipe.session.framework.flask import verify_session

from ..Utility_Function import validate

blueprint: Blueprint = Blueprint("student_add", __name__)


@blueprint.route("/add", methods=["POST"])
@verify_session()
def student_add() -> dict:
    status = "success"
    msg = "OK"
    data = request.get_json()

    student = {
        "email": data["email"],
        "password": data["password"],
        "fname_en": data["fname_en"],
        "mname_en": data["mname_en"],
        "lname_en": data["lname_en"],
        "fname_th": data["fname_th"],
        "mname_th": data["mname_th"],
        "lname_th": data["lname_th"],
        "student_id": data["student_id"],
    }
    tag_list = [
        "fname_en",
        "mname_en",
        "lname_en",
        "fname_th",
        "mname_th",
        "lname_th",
    ]
    student["academic_year"] = int("25" + student["student_id"][:2]) - 543
    status, msg = validate(tag_list, data)
    if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
        return {
            "status": "Error",
            "msg": msg,
        }
    cursor = db.cursor()

    """check student id not signup yet"""
    query = """SELECT student_id FROM `student` WHERE student_id IN (%s);"""
    cursor.execute(query, [int(student["student_id"])])
    result = cursor.fetchone()
    if result is not None:
        return {
            "status": "Error",
            "msg": "student id already sign up",
        }

    """signup supertoken and getuser_id"""
    sign_up(student["email"], student["password"])
    users_info = get_user_by_email(student["email"])
    user_id = users_info.user_id

    """insert to user and student table"""
    list_user = [
        [
            user_id,
            "student",
            student["email"],
            student["fname_th"],
            student["mname_th"],
            student["lname_th"],
            student["fname_en"],
            student["mname_th"],
            student["lname_th"],
        ],
        [user_id, student["student_id"], student["academic_year"]],
    ]
    query_user = [
        """INSERT INTO user(user_id, type, email, fname_th,mname_th, lname_th, fname_en, mname_en, lname_en) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        """INSERT INTO student(user_id, student_id, academic_year) VALUES (%s,%s,%s)""",
    ]
    for i in range(2):
        cursor.execute(query_user[i], list_user[i])
        db.commit()
    return {
        "status": status,
        "msg": "user {0} name {1} is success!".format(
            student["student_id"], student["fname_th"]
        ),
    }
