from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("course_category_add", __name__)


@blueprint.route("/add", methods=["POST"])
def course_category_add() -> dict:
    dataes = request.get_json()

    result = []
    if len(dataes) != 5:
        return {"status": "fail", "msg": "need to fill all information"}
    for data in dataes:
        if dataes.get(data) == "":
            return {"status": "fail", "msg": "please input value"}
        else:
            result.append(dataes.get(data))
    tempq = "SELECT id FROM course_category"
    query = "INSERT INTO course_category (id,name_th,name_en,abbr_th,abbr_en) VALUES (%s, %s, %s, %s, %s)"
    mycursor = db.cursor()

    mycursor.execute(tempq)
    q = mycursor.fetchall()

    if len(q) < result[0]:
        if result[0] > len(q) + 1:
            return {
                "status": "fail",
                "msg": "please change id to " + str(len(q) + 1),
            }
        else:
            mycursor.execute(query, result)
            db.commit()
            return {
                "status": "success",
                "msg": "new category have been add.",
                "id": result[0],
                "name_th": result[1],
                "name_en": result[2],
                "abbr_th": result[3],
                "abbr_en": result[4],
            }

    else:
        if result[0] >= len(q) + 1:
            return {"revalue": "revalue"}
        else:
            return {
                "status": "error",
                "msg": "please change id to " + str(len(q) + 1),
            }
