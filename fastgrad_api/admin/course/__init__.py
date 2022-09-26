from flask import Blueprint

from . import course_browse

blueprint: Blueprint = Blueprint("course", __name__)

blueprint.register_blueprint(course_browse.blueprint)
