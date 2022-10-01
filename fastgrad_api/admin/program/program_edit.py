from database import db
from flask import Blueprint, request

from .Utility_Function_program import checkyear, nonecheck

blueprint: Blueprint = Blueprint("program_edit", __name__)


@blueprint.route("/program_edit/<program_id>", methods=["GET", "POST"])
async def program_browse(program_id) -> dict:
    status = "success"
    msg = "ok"
    results = []
    listyear = ["start_year", "end_year"]
    listpro = ["name_th", "name_en"]
    datas = request.get_json()

    status, msg = checkyear(listyear, datas)
    if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
        return msg
    status, msg = nonecheck(listpro, datas)
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
