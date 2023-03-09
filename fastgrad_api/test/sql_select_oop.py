from typing import List

from database import db
from flask import Blueprint, request
from route import Route, register_route

blueprint: Blueprint = Blueprint("test_select_oop", __name__)


class SelectCourse(Route):
    def __init__(self) -> None:
        super().__init__(path="/sql_select_oop", methods=["GET"])

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

        return {
            "status": "success",
            "msg": "OK",
            "data": [
                {col: row[i] for i, col in enumerate(cols)} for row in result
            ],
        }

    def post(self, *args, **kwargs):
        """Leave this blank to indicate that there is really no use of POST method here"""


_routes: List[Route] = [
    SelectCourse(),
]

register_route(blueprint, _routes)
