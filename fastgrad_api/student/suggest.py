from database import db
from flask import Blueprint, request, request_finished
from supertokens_python.recipe.session.framework.flask import verify_session

from . import utility

blueprint: Blueprint = Blueprint("/suggest", __name__)

""""
Utility Functions
#################

"""


# Random Course that have equivilent weight
def randomFromAction(id):
    return


# Find course
def findCourse():
    return


"""_summary_
the request body must look like this
course: number 
while number in range (1,6)
Returns:
    _type_: _description_
"""


# @blueprint.route("/suggest", methods=["GET"])
# def suggest() -> dict:
#     all_course = utility.getCourse()
#     learned_course = utility.getUserEnrollment()
#     # possible_course = utility.findCourse(learned_course, all_course)
#     return {"course": learned_course}


@blueprint.route("/suggest", methods=["POST"])
@verify_session()
def postSuggest() -> dict:
    req = request.args.to_dict()
    all_course = utility.getCourse(req["plan"])
    learned_course = utility.getUserEnrollment(req["student_id"])
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    return {
        "total_course": len(learned_course),
        "learned_course": learned_course,
    }


@blueprint.route("/trytotest", methods=["GET"])
def testStudent() -> dict:
    all_course = utility.getCourse()
    # learned_course = utility.getUserEnrollment()
    # possible_course = utility.findPossibleCourse(learned_course, all_course)result = utility.getPlanRequirment()
    # result = utility.findPossibleCourse(learned_course, all_course)
    return {"course": all_course}
