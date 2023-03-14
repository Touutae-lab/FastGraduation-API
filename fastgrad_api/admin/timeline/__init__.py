from flask import Blueprint

from . import timeline

blueprint: Blueprint = Blueprint("timeline", __name__)

blueprint.register_blueprint(timeline.blueprint)
