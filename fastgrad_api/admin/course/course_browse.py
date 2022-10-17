from database import db
from flask import Blueprint, request
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("course_browse", __name__)


@verify_session()
@blueprint.route("/browse", methods=["GET"])
async def browse_course() -> dict:
    query = "SELECT * FROM course"
    params = request.args.to_dict()
    if "q" in params:
        query += (
            f" WHERE id LIKE '%{params['q']}%' OR name_th LIKE "
            f"'%{params['q']}%' OR name_en LIKE '%{params['q']}%' "
            f" OR description_th LIKE '%{params['q']}%' OR description_en LIKE'%{params['q']}%'"
        )

    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    # Not Found
    if result == []:
        return {"status": "error", "msg": "Not Found "}

    cols = [i[0] for i in cursor.description]

    return {
        "status": "success",
        "msg": "OK",
        "data": [
            {col: row[i] for i, col in enumerate(cols)} for row in result
        ],
    }
