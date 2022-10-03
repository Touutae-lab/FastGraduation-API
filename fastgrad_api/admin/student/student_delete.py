# from database import db
# from flask import Blueprint, request,Flask, g

# from supertokens_python.recipe.session.framework.flask import verify_session
# from supertokens_python.recipe.emailpassword.syncio import get_user_by_id

# from supertokens_python.recipe.session import SessionContainer
# blueprint: Blueprint = Blueprint("student_delete", __name__)

# @blueprint.route("/student/delete", methods=["GET"])
# @verify_session()
# def student_delete() ->dict:
#     session: SessionContainer = g.supertokens
#     user_id = session.get_user_id()
#     return user_id
