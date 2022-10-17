from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("add_category", __name__)


@blueprint.route("/add", methods=["POST"])
@verify_session()
def category_add() -> dict:
    dataes = request.get_json()

    result = []
    for data in dataes:
        result.append(dataes.get(data))
    query = "INSERT INTO course_category (id,name_th,name_en,abbr_th,abbr_en) VALUES (%s, %s, %s, %s, %s)"
    mycursor = db.cursor()
    mycursor.execute(query, result)
    db.commit()

    return {
        "status": "success",
        "msg": "new category have been add.",
        "result": result,
    }
