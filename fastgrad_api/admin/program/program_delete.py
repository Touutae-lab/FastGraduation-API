from database import db
from flask import Blueprint
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("program_delete", __name__)


@blueprint.route("/delete/<program_id>", methods=["GET"])
@verify_session()
def student_delete(program_id) -> dict:
    status = "success"
    msg = "ok"
    query = """DELETE FROM program WHERE id =""" + str(program_id)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

    if cursor.rowcount == 0:  # ลบความว่างเปล่า
        msg = "0 record(s) deleted , check your program id agian"
    else:
        msg = (cursor.rowcount, "record(s) deleted")
    return {"status": status, "massage": msg}
