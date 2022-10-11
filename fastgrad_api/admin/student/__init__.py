from flask import Blueprint

from . import student__add, student_browse, student_delete, student_edit

blueprint: Blueprint = Blueprint("student", __name__)

blueprint.register_blueprint(student_browse.blueprint)
blueprint.register_blueprint(student_edit.blueprint)
blueprint.register_blueprint(student__add.blueprint)
blueprint.register_blueprint(student_delete.blueprint)
