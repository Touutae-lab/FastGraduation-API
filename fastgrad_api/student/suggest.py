from flask import Blueprint, request

from . import utility

blueprint: Blueprint = Blueprint("/suggest", __name__)

rank: list = [5, 4, 3]


# Random Course that have equivilent weight
def randomFromAction(id):
    return


# Find course
def findCourse():
    return


@blueprint.route("/suggest", methods=["POST"])
async def postSuggest() -> dict:
    """_summary_
    the request body must look like this
    course: number
    while number in range (1,6)
    Returns:
        _type_: _description_
    """

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

    return {"term_1": term_1, "term_2": term_2}


@blueprint.route("/trytotest", methods=["GET"])
async def testStudent() -> dict:
    learned_course = utility.getUserEnrollment("630510501")
    all_course = utility.getCourse()
    possible_course = utility.findPossibleCourse(learned_course, all_course)

    requirement = utility.getPlanRequirment()
    term_1 = utility.suggestion(possible_course, requirement, learned_course)
    for i in term_1:
        learned_course.append(utility.getCategory(i)[0])

    possible_course = utility.findPossibleCourse(learned_course, all_course)
    term_2 = utility.suggestion(possible_course, requirement, learned_course)
    return {"term_1": term_1, "term_2": term_2}


@blueprint.route("/available_course", methods=["POST"])
async def avalable_course() -> dict:
    req = request.args.to_dict()
    learned_course = utility.getUserEnrollment(req["student_id"])
    all_course = utility.getCourse(req["plan_id"])
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    return {"course": possible_course}
