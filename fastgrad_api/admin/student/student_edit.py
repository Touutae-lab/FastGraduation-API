from database import db
from flask import Blueprint, request

from .Utility_Function import checklanguage

blueprint: Blueprint = Blueprint("student_edit", __name__)


@blueprint.route("/edit/<student_id>", methods=["GET", "POST"])
async def student_browse(student_id) -> dict:
    status = "success"
    msg = "ok"

    en_list = ["fname_en", "mname_en", "lname_en"]
    th_list = ["fname_th", "mname_th", "lname_th"]
    if request.method == "POST":
        data = request.get_json()
        if not student_id.isdigit() or len(student_id) != 9:
            status = "failure"
            msg = "invaild student id"
            return {"status": status, "msg": msg}

        else:  # เอาไว้ตรวจดูว่าเขียนภาษามาถูกไหม
            status, msg = checklanguage(en_list, data)
            if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
                return msg
            status, msg = checklanguage(th_list, data)
            if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
                return msg

        if data.get("mname_en") is None:

            query = """UPDATE student
                    INNER JOIN user ON student.user_id =user.user_id
                    SET fname_en='%(fname_en)s',mname_en =null ,lname_en='%(lname_en)s',fname_th='%(fname_th)s',mname_th=null,lname_th='%(lname_th)s',email='%(email)s'
                    WHERE student_id='%(student_id)s' """ % {
                "fname_en": data.get("fname_en"),
                "lname_en": data.get("lname_en"),
                "fname_th": data.get("fname_th"),
                "lname_th": data.get("lname_th"),
                "email": data.get("email"),
                "student_id": student_id,
            }
        else:
            query = """UPDATE student
                    INNER JOIN user ON student.user_id =user.user_id
                    SET fname_en='%(fname_en)s',mname_en ='%(mname_en)s' ,lname_en='%(lname_en)s',fname_th='%(fname_th)s',mname_th='%(mname_th)s',lname_th='%(lname_th)s',email='%(email)s'
                    WHERE student_id='%(student_id)s' """ % {
                "fname_en": data.get("fname_en"),
                "mname_en": data.get("mname_en"),
                "lname_en": data.get("lname_en"),
                "fname_th": data.get("fname_th"),
                "mname_th": data.get("mname_th"),
                "lname_th": data.get("lname_th"),
                "email": data.get("email"),
                "student_id": student_id,
            }

        cursor = db.cursor()
        cursor.execute(query)

        db.commit()

    query = (
        "SELECT student_id,fname_en,mname_en,lname_en,fname_th,mname_th,lname_th,email,academic_year FROM user ,student WHERE  user.user_id=student.user_id AND student_id ="
        + student_id
    )

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()[0]
    (
        student_id,
        fname_en,
        mname_en,
        lname_en,
        fname_th,
        mname_th,
        lname_th,
        email,
        *_,
    ) = result
    return {
        "status": status,
        "msg": msg,
        "data": {
            "student_id": student_id,
            "first_name_en": fname_en,
            "mid_name_en": mname_en,
            "last_name_en": lname_en,
            "first_name_th": fname_th,
            "mid_name_th": mname_th,
            "last_name_th": lname_th,
            "email": email,
        },
    }
