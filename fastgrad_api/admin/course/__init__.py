from flask import Blueprint

from . import course_browse, course_edit, course_delete, course_add

blueprint: Blueprint = Blueprint("course", __name__)
blueprint.register_blueprint(course_browse.blueprint)
blueprint.register_blueprint(course_edit.blueprint)
blueprint.register_blueprint(course_delete.blueprint)
blueprint.register_blueprint(course_add.blueprint)
