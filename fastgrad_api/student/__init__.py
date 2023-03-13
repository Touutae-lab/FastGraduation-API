from flask import Blueprint

from . import browse_course, missing_credits, suggest, update_enrollment

blueprint: Blueprint = Blueprint("student", __name__)

blueprint.register_blueprint(browse_course.blueprint)
blueprint.register_blueprint(update_enrollment.blueprint)
blueprint.register_blueprint(suggest.blueprint)
blueprint.register_blueprint(missing_credits.blueprint)