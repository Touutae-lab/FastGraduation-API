from flask import Blueprint

from . import add_category, browse_category, delete_category, edit_category

blueprint: Blueprint = Blueprint("course_category", __name__)
blueprint.register_blueprint(add_category.blueprint)
blueprint.register_blueprint(browse_category.blueprint)
blueprint.register_blueprint(delete_category.blueprint)
blueprint.register_blueprint(edit_category.blueprint)
