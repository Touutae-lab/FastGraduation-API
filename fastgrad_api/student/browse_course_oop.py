from typing import List

from database import db_oop as db
from flask import Blueprint, request
from route import Route, register_route
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("browse_course_oop", __name__)


class BrowseCourse(Route):
    def __init__(self) -> None:

        super().__init__(path="/browse_course_oop", methods=["GET"])

    @verify_session()
    def get(self, *args, **kwargs):
        query = "SELECT * FROM course"
        params = request.args.to_dict()
        if "q" in params:
            query += (
                " WHERE id LIKE %s OR name_th LIKE "
                "%s OR name_en LIKE %s "
                " OR description_th LIKE %s OR description_en LIKE %s"
            )

        q = params.get("q")
        cursor, _ = db.execute(query, [] if q is None else ["%" + q + "%"] * 5)

        result = cursor.fetchall()
        # Not Found
        if result == []:
            return {"status": "error", "msg": "Not Found "}

        cols = [i[0] for i in cursor.description]
        col_cat = [i[0] for i in cursor.description]
        res_cat = cursor.fetchall()
        return {
            "status": "success",
            "msg": "OK",
            "data": [
                {col: row[i] for i, col in enumerate(cols)} for row in result
            ],
            "categories": [
                {col: row[i] for i, col in enumerate(col_cat)}
                for row in res_cat
            ],
        }

    # def post(self, *args, **kwargs):
    #     """Leave this blank to indicate that there is really no use of POST method here"""


_routes: List[Route] = [
    BrowseCourse(),
]

register_route(blueprint, _routes)
