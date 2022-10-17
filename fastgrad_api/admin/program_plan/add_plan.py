from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("add_plan", __name__)


@blueprint.route("/add", methods=["POST"])
@verify_session()
def category_add() -> dict:
    dataes = request.get_json()

    result = []
    for data in dataes:
        result.append(dataes.get(data))
    query = "INSERT INTO plan (id,program_id,name_th,name_en,min_credit,is_for_all) VALUES (%s, %s, %s, %s, %s,%s)"
    mycursor = db.cursor()
    mycursor.execute(query, result)
    db.commit()

    return {
        "status": "success",
        "msg": "new plan have been add.",
        "id": result[0],
        "program_id": result[1],
        "name_th": result[2],
        "name_en": result[3],
        "min_credit": result[4],
        "is_for_all": result[5],
    }
