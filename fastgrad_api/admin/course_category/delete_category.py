from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("delete_category", __name__)


@blueprint.route("/course_category/delete/<category_id>", methods=["GET"])
async def category_delete(category_id) -> dict:
    query = "DELETE FROM course_category WHERE id = "
    params = request.args.to_dict()
    if "q" in params:
        query += params["q"]

    cursor = db.cursor()
    cursor.execute(query)

    db.commit()

    return {
        "status": "success",
        "msg": "record have been deleted.",
    }
