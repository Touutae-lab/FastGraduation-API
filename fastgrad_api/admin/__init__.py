from flask import Blueprint

from . import student

blueprint: Blueprint = Blueprint("admin", __name__)

blueprint.register_blueprint(student.blueprint, url_prefix="/student")
