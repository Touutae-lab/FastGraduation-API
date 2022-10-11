from flask import Blueprint

from . import add_plan, browse_plan, delete_plan, edit_plan

blueprint: Blueprint = Blueprint("program_plan", __name__)

blueprint.register_blueprint(add_plan.blueprint)
blueprint.register_blueprint(browse_plan.blueprint)
blueprint.register_blueprint(delete_plan.blueprint)
blueprint.register_blueprint(edit_plan.blueprint)
