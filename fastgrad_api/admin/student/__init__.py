from flask import Blueprint

from . import student_browse, student_edit

blueprint: Blueprint = Blueprint("student", __name__)

blueprint.register_blueprint(student_browse.blueprint)
blueprint.register_blueprint(student_edit.blueprint)
