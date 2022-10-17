from flask import Blueprint

from . import program_add, program_browse, program_delete, program_edit

blueprint: Blueprint = Blueprint("admin", __name__)
blueprint.register_blueprint(program_add.blueprint)
blueprint.register_blueprint(program_browse.blueprint)
blueprint.register_blueprint(program_edit.blueprint)
blueprint.register_blueprint(program_delete.blueprint)
