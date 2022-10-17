from flask import Blueprint

from . import course_category, program_plan

blueprint: Blueprint = Blueprint("admin", __name__)


blueprint.register_blueprint(
    program_plan.blueprint, url_prefix="/program_plan"
)
blueprint.register_blueprint(
    course_category.blueprint, url_prefix="/course_category"
)
