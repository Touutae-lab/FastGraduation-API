from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

from ..Utility_Function import validate

blueprint: Blueprint = Blueprint("program_add", __name__)


@blueprint.route("/add", methods=["POST"])
@verify_session()
async def program_add() -> dict:
    status = "success"
    msg = "ok"
    datas = request.get_json()
    results = []
    listpro = ["start_year", "end_year", "name_th", "name_en"]

    status, msg = validate(listpro, datas)
    if not status:  # ถ้าไม่ถูกให้ returnfalse พร้อม สาเหตุ
        return msg

    # find max index
    index_program = """SELECT max(id)+1 as maxid FROM program"""
    cursor = db.cursor()
    cursor.execute(index_program)
    result = cursor.fetchall()[0]
    for i in result:
        index_program_new = i
    results.append(index_program_new)

    for data in datas:
        results.append(datas.get(data))

    query = """INSERT INTO program(id,start_year,end_year,name_th,name_en)
             VAlUES (%s,%s,%s,%s,%s)"""
    cursor = db.cursor()
    cursor.execute(query, results)
    db.commit()

    query = "SELECT * FROM program where id =" + str(index_program_new)
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
