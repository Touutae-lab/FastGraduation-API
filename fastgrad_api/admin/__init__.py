from flask import Blueprint

from . import course, program, student

blueprint: Blueprint = Blueprint("admin", __name__)

blueprint.register_blueprint(student.blueprint, url_prefix="/student")
blueprint.register_blueprint(course.blueprint, url_prefix="/course")
blueprint.register_blueprint(program.blueprint, url_prefix="/program")
