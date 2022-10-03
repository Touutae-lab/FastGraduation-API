from flask import Blueprint

from . import course, program, student
from .course_category import (
    add_category,
    browse_category,
    delete_category,
    edit_category,
)
from .program_plan import add_plan, browse_plan, delete_plan, edit_plan

blueprint: Blueprint = Blueprint("admin", __name__)
blueprint.register_blueprint(student.blueprint, url_prefix="/student")
blueprint.register_blueprint(course.blueprint, url_prefix="/course")
blueprint.register_blueprint(program.blueprint, url_prefix="/program")


blueprint.register_blueprint(browse_category.blueprint)
blueprint.register_blueprint(delete_category.blueprint)
blueprint.register_blueprint(add_category.blueprint)
blueprint.register_blueprint(edit_category.blueprint)

blueprint.register_blueprint(browse_plan.blueprint)
blueprint.register_blueprint(add_plan.blueprint)
blueprint.register_blueprint(delete_plan.blueprint)
blueprint.register_blueprint(edit_plan.blueprint)
