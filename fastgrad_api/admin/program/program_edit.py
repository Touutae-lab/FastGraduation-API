from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

from ..Utility_Function import validate

blueprint: Blueprint = Blueprint("program_edit", __name__)


@blueprint.route("/program_edit/<program_id>", methods=["GET", "POST"])
@verify_session()
def program_browse(program_id) -> dict:
    status = "success"
    msg = "ok"
    results = []
    tag_list = ["year_start", "year_end", "name_th", "name_en"]
    datas = request.get_json()

    status, msg = validate(tag_list, datas)
    if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
        return msg

    if request.method == "POST":

        for data in datas:
            results.append(datas.get(data))

        query = (
            """UPDATE program SET start_year=%s,end_year=%s,name_th=%s,name_en=%s WHERE id="""
            + str(program_id)
        )
        cursor = db.cursor()
        cursor.execute(query, results)
        db.commit()
        cursor = db.cursor()
        query = """select * from program where id=""" + str(program_id)
        cursor.execute(query)
        result = cursor.fetchall()

    return {
        "status": status,
        "msg": msg,
        "data": [
            {
                "id": index,
                "start_year": start_year,
                "end_year": end_year,
                "name_th": name_th,
                "name_en": name_en,
            }
            for index, start_year, end_year, name_th, name_en, *_ in result
        ],
    }
