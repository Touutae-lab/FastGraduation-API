import random

from pkg_resources import require

from database import db
from flask import Blueprint, request, request_finished
from supertokens_python.recipe.session.framework.flask import verify_session

from . import utility

blueprint: Blueprint = Blueprint("/suggest", __name__)

rank: list = [5, 4, 3]


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
async def postSuggest() -> dict:
    req = request.args.to_dict()
    
    all_course = utility.getCourse(req["plan_id"])
    learned_course = utility.getUserEnrollment(req["student_id"])
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    requirement = utility.getPlanRequirment(req["plan_id"])

    term_1 = utility.suggestion(possible_course, requirement, learned_course)
    
    for i in term_1:
        learned_course.append(utility.getCategory(i)[0])
    
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    term_2 = utility.suggestion(possible_course, requirement, learned_course)
    
    return {
        "term_1": term_1,
        "term_2": term_2
    }


@blueprint.route("/trytotest", methods=["GET"])
async def testStudent() -> dict:
    learned_course = utility.getUserEnrollment("630510501")
    all_course = utility.getCourse()
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    
    requirement = utility.getPlanRequirment()
    # test = utility.diffRequirment(requirement, learned_course)
    
    term_1 = utility.suggestion(possible_course, requirement, learned_course)
    
    for i in term_1:
        learned_course.append(utility.getCategory(i)[0])
    
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    term_2 = utility.suggestion(possible_course, requirement, learned_course)
    return {"term_1": term_1,
            "term_2": term_2
            }


@blueprint.route("/available_course", methods=["POST"])
async def avalable_course() -> dict:
    req = request.args.to_dict()
    learned_course = utility.getUserEnrollment(req["student_id"])
    all_course = utility.getCourse(req["plan_id"])
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    return {"course": possible_course}


@blueprint.route("/should_learn", methods=["GET"])
def should_learn() -> dict:
    
    return
