from flask import Blueprint

from . import (
    course_category_add,
    course_category_browse,
    course_category_delete,
    course_category_edit,
)

blueprint: Blueprint = Blueprint("course_category", __name__)
blueprint.register_blueprint(course_category_add.blueprint)
blueprint.register_blueprint(course_category_browse.blueprint)
blueprint.register_blueprint(course_category_edit.blueprint)
blueprint.register_blueprint(course_category_delete.blueprint)
