from database import db
from flask import Blueprint, request

blueprint: Blueprint = Blueprint("course_category_delete", __name__)


@blueprint.route("/delete/<category_id>", methods=["GET"])
def ccourse_category_delete(category_id) -> dict:
    query = "DELETE FROM course_category WHERE id = "
    params = request.args.to_dict()
    if "category_id" in params:
        query += params["category_id"]
    else:
        return {"status": "fail", "msg": "not found this category id"}

    cursor = db.cursor()
    cursor.execute(query)

    db.commit()

    return {
        "status": "success",
        "msg": "record have been deleted.",
    }
