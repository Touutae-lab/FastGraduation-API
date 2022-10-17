from flask import Blueprint

from . import plan_add, plan_browse, plan_delete, plan_edit

blueprint: Blueprint = Blueprint("plan", __name__)
blueprint.register_blueprint(plan_add.blueprint)
blueprint.register_blueprint(plan_browse.blueprint)
blueprint.register_blueprint(plan_edit.blueprint)
blueprint.register_blueprint(plan_delete.blueprint)
