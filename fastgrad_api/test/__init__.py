from flask import Blueprint

from . import sql_select_oop, sql_update, test_new_route

blueprint: Blueprint = Blueprint("test", __name__)
blueprint.register_blueprint(sql_update.blueprint)
blueprint.register_blueprint(test_new_route.blueprint)
blueprint.register_blueprint(sql_select_oop.blueprint)
