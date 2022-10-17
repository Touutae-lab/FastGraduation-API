from database import db
from flask import Blueprint
from supertokens_python.recipe.session.framework.flask import verify_session
from supertokens_python.syncio import delete_user

blueprint: Blueprint = Blueprint("student_delete", __name__)


@blueprint.route("/delete/<student_id>", methods=["GET"])
@verify_session()
def student_delete(student_id) -> dict:
    status = "success"
    msg = "ok"
    userid = ""
    useridx = ""
    count = 0

    query_user_id = """SELECT student.user_id FROM `student`
                      JOIN user ON user.user_id=student.user_id
                      WHERE student.student_id=""" + str(
        student_id
    )
    cursor = db.cursor()
    cursor.execute(query_user_id)
    userid = cursor.fetchall()

    if userid == []:
        return {"status": "error", "massage": "not found"}
    for i in userid[0]:
        useridx = i

    delete_list = {
        "query_delete_enr": """DELETE FROM `enrollment` WHERE student_id ="""
        + str(student_id),
        "query_delete_st": """DELETE student FROM student WHERE  student_id="""
        + str(student_id),
    }
    for i in delete_list:
        cursor.execute(delete_list[i])
        db.commit()
        count += cursor.rowcount

    query_delete_user = """DELETE FROM `user` WHERE user_id=%s"""
    cursor.execute(query_delete_user, [useridx])
    db.commit()
    count += cursor.rowcount

    delete_user(useridx)

    if cursor.rowcount == 0:  # ลบความว่างเปล่า
        msg = "0 record(s) deleted , check your student_id agian"
    else:
        msg = (count, "record(s) deleted")
    return {"status": status, "massage": msg}
