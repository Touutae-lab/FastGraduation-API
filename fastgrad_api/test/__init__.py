from flask import Blueprint

from . import sql_update

blueprint: Blueprint = Blueprint("test", __name__)
blueprint.register_blueprint(sql_update.blueprint)
