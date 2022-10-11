from flask import Blueprint

from . import browse_course, profile, update_enrollment

blueprint: Blueprint = Blueprint("student", __name__)

blueprint.register_blueprint(browse_course.blueprint)
blueprint.register_blueprint(update_enrollment.blueprint)
blueprint.register_blueprint(profile.blueprint)
