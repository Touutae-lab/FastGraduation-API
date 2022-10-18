from flask import Blueprint

from . import course, course_category, program, program_plan, student

blueprint: Blueprint = Blueprint("admin", __name__)


blueprint.register_blueprint(
    program_plan.blueprint, url_prefix="/program_plan"
)
blueprint.register_blueprint(
    course_category.blueprint, url_prefix="/course_category"
)
blueprint.register_blueprint(course.blueprint, url_prefix="/course")
blueprint.register_blueprint(program.blueprint, url_prefix="/student")
blueprint.register_blueprint(student.blueprint, url_prefix="/program")
