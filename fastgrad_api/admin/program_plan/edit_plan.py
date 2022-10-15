from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("edit_plan", __name__)


@blueprint.route("/edit/<plan_id>", methods=["GET", "POST"])
@verify_session()
def plan_edit(plan_id: int) -> dict:

    dataes = request.get_json()

    result = []

    for data in dataes:
        result.append(dataes.get(data))
        query = "SELECT * FROM plan WHERE id = " + str(result[0])
    mycursor = db.cursor()
    mycursor.execute(query)
    temp = mycursor.fetchall()
    query = "SELECT * FROM plan WHERE id = " + str(result[0])
    for i in range(len(result)):
        if i == 2:
            query = (
                "UPDATE plan SET name_th = "
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
                "UPDATE plan SET name_en = "
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
                "UPDATE plan SET min_credit = "
                + "'"
                + str(result[i])
                + "' "
                + "WHERE id = "
                + str(result[0])
            )
            mycursor = db.cursor()
            mycursor.execute(query)
            db.commit()

    # query = []
    # sql = "UPDATE plan SET name_th = %s,name_en = %s,abbr_th = %s,abbr_en = %s WHERE id = %s" + str(result[0])
    # for i in range(1,len(result)):
    #     query.append(result[i])
    # mycursor = db.cursor()
    # mycursor.execute(sql,query)
    # db.commit()

    return {
        "status": "success",
        "msg": "category info have been updated.",
        "id": result[0],
        "new_program_id": temp[1],
        "new_name_th": temp[2],
        "new_name_en": temp[3],
        "new_min_credit": temp[4],
        "name_th": result[2],
        "name_en": result[3],
        "min_credit": result[4],
    }
