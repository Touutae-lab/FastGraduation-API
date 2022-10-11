from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("course_category_edit", __name__)


@blueprint.route("/edit/<category_id>", methods=["GET", "POST"])
def course_category_edit(category_id) -> dict:

    dataes = request.get_json()

    result = []

    for data in dataes:
        result.append(dataes.get(data))
    for i in range(len(result)):
        if i == 1:
            query = (
                "UPDATE course_category SET name_th = "
                + "'"
                + result[i]
                + "' "
                + "WHERE id = "
                + str(result[0])
            )
            mycursor = db.cursor()
            mycursor.execute(query)
            db.commit()
        if i == 2:
            query = (
                "UPDATE course_category SET name_en = "
                + "'"
                + result[i]
                + "' "
                + "WHERE id = "
                + str(result[0])
            )
            mycursor = db.cursor()
            mycursor.execute(query)
            db.commit()
        if i == 3:
            query = (
                "UPDATE course_category SET abbr_th = "
                + "'"
                + result[i]
                + "' "
                + "WHERE id = "
                + str(result[0])
            )
            mycursor = db.cursor()
            mycursor.execute(query)
            db.commit()
        if i == 4:
            query = (
                "UPDATE course_category SET abbr_en = "
                + "'"
                + result[i]
                + "' "
                + "WHERE id = "
                + str(result[0])
            )
            mycursor = db.cursor()
            mycursor.execute(query)
            db.commit()

    # query = []
    # sql = "UPDATE course_category SET name_th = %s,name_en = %s,abbr_th = %s,abbr_en = %s WHERE id = %s" + str(result[0])
    # for i in range(1,len(result)):
    #     query.append(result[i])
    # mycursor = db.cursor()
    # mycursor.execute(sql,query)
    # db.commit()

    return {
        "status": "success",
        "msg": "category info have been updated.",
        "id": result[0],
    }
