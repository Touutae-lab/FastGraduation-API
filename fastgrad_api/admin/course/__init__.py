from flask import Blueprint

from . import course_browse, course_edit

blueprint: Blueprint = Blueprint("course", __name__)
blueprint.register_blueprint(course_browse.blueprint)
blueprint.register_blueprint(course_edit.blueprint)
