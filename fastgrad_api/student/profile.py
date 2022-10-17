from database import db
from flask import Blueprint, g
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("profile", __name__)


@blueprint.route("/profile", methods=["GET"])
@verify_session()
def profile() -> dict:
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()

    query = """SELECT student_id,fname_en,mname_en,lname_en,fname_th,mname_th,lname_th,email,academic_year
    FROM user ,student WHERE user.user_id=student.user_id AND user.user_id=%s  """

    cursor = db.cursor()
    cursor.execute(query, [user_id])
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
                "academic_year": academic_year,
            }
            for student_id, fname_en, mname_en, lname_en, fname_th, mname_th, lname_th, email, academic_year, *_ in result
        ],
    }
