from database import db_oop as db
from flask import Blueprint
from route import Route, register_route

blueprint: Blueprint = Blueprint("timeline_browse", __name__)


class Timeline(Route):
    def __init__(self) -> None:
        super().__init__(
            path=[("/browse/<program_id>", None)],
            methods=["GET", "POST"],
        )

    def fetchTimeline(self, program_id):
        ret = []

        # get course
        cursor, _ = db.execute(
            "SELECT * FROM default_timeline_course WHERE program_id = %s",
            [program_id],
        )
        result = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        ret.extend(
            [{col: row[i] for i, col in enumerate(cols)} for row in result]
        )

        # get category
        cursor, _ = db.execute(
            "SELECT * FROM default_timeline_category WHERE program_id = %s",
            [program_id],
        )
        result = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        ret.extend(
            [{col: row[i] for i, col in enumerate(cols)} for row in result]
        )

        # get course with plan
        cursor, _ = db.execute(
            "SELECT plan.program_id, default_timeline_plan_course.plan_id, course_id, term, year FROM `default_timeline_plan_course` JOIN plan ON default_timeline_plan_course.plan_id = plan.id WHERE program_id = %s",
            [program_id],
        )
        result = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        ret.extend(
            [{col: row[i] for i, col in enumerate(cols)} for row in result]
        )

        # get category with plan
        cursor, _ = db.execute(
            (
                "SELECT plan.program_id, "
                "default_timeline_plan_category.plan_id, cat_id, term, year "
                "FROM `default_timeline_plan_category` JOIN plan "
                "ON default_timeline_plan_category.plan_id = plan.id "
                "WHERE program_id = %s"
            ),
            [program_id],
        )
        result = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        ret.extend(
            [{col: row[i] for i, col in enumerate(cols)} for row in result]
        )

        return ret

    def get(self, *args, **kwargs):
        program_id = kwargs.get("program_id", None)
        return self.fetchTimeline(program_id)

    def post(self, *args, **kwargs):
        pass


register_route(blueprint, Timeline())
