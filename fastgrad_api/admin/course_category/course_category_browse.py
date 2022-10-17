from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_category_browse", __name__)


@blueprint.route("/browse", methods=["GET"])
@verify_session()
def browse_category() -> dict:
    query = "SELECT * FROM course_category"
    params = request.args.to_dict()

    if "q" in params:
        query += (
            f" WHERE id LIKE '%{params['q']}%' OR name_th LIKE "
            f"'%{params['q']}%' OR name_en LIKE '%{params['q']}%'"
        )

    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    if result == []:
        return {"status": "success", "msg": "not found"}
    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {
                "category_id": id,
                "category_name_th": name_th,
                "category_name_en": name_en,
                "description_th": abbr_th,
                "description_en": abbr_en,
            }
            for id, name_th, name_en, abbr_th, abbr_en, *_ in result
        ],
    }
