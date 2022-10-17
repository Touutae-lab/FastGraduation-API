from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("plan_add", __name__)


@blueprint.route("/add", methods=["POST"])
def plan_add() -> dict:
    dataes = request.get_json()

    result = []

    if len(dataes) != 5:
        return {"status": "fail", "msg": "need to fill all information"}
    for data in dataes:
        if dataes.get(data) == "":
            return {"status": "fail", "msg": "please input value"}
        else:
            result.append(dataes.get(data))
    tempq = "SELECT id FROM plan"
    query = "INSERT INTO plan (id,program_id,name_th,name_en,min_credit) VALUES ( %s,%s, %s, %s, %s)"

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
                "program_id": result[1],
                "name_th": result[2],
                "name_en": result[3],
                "min_credit": result[4],
            }

    else:
        if result[0] >= len(q) + 1:
            return {"revalue": "revalue"}
        else:
            return {
                "status": "error",
                "msg": "please change id to " + str(len(q) + 1),
            }

    # tempq = "SELECT id FROM plan"
    # mycursor.execute(tempq)
    # q = mycursor.fetchall()
    # emptId = []
    # emptId.append(result[0])
    # if  emptId not in q:
    #     if emptId not in q:
    #         return {"q" : q}
    #     else :
    #         # mycursor.execute(query, result)
    #         # db.commit()
    #         return {
    #             "status": "success",
    #             "msg": "new plan have been add.",
    #             "id": result[0],
    #             "program_id": result[1],
    #             "name_th": result[2],
    #             "name_en": result[3],
    #             "min_credit": result[4]

    #     }

    # else :

    #     return {
    #     "status": "fail",
    #     "msg": "alreaydy have this id."}


# from database import db
# from flask import Blueprint, request

# blueprint: Blueprint = Blueprint("add_plan", __name__)


# @blueprint.route("/plan/add", methods=["POST"])
# async def category_add() -> dict:
#     dataes = request.get_json()

#     result = []
#     for data in dataes:
#         result.append(dataes.get(data))
#     query = "INSERT INTO plan_requirement (plan_id,category_id,min_credit) VALUES ( %s, %s, %s)"
#     mycursor = db.cursor()
#     mycursor.execute(query, result)
#     db.commit()

#     return {
#         "status": "success",
#         "msg": "new plan have been add.",
#         "id": result
#     }
