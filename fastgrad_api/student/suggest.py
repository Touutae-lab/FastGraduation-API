from flask import Blueprint, g
from route import Route
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

from . import utility

blueprint: Blueprint = Blueprint("suggest", __name__)

rank: list = [5, 4, 3]

# class UserDefine:
#     self.data
#     self.naruto
#     self.dice
class Suggestion(Route):
    def __init__(self) -> None:
        super().__init__(path="/suggest", methods=["GET"])

    @verify_session()
    def get(self, *args, **kwargs) -> dict:
        session: SessionContainer = g.supertokens

        return {"A": session.get_user_id()}


# Random Course that have equivilent weight
def randomFromAction(id):
    return


# Find course
def findCourse():
    return


@blueprint.route("/suggest", methods=["GET"])
@verify_session()
def postSuggest() -> dict:
    """_summary_
    the request body must look like this
    course: number
    while number in range (1,6)
    Returns:
        _type_: _description_
    """

    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()
    student_id = utility.getStudentId(user_id)
    plan_id = utility.getPlanId(student_id)

    all_course = utility.getCourse(plan_id)
    learned_course = utility.getUserEnrollment(student_id)
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    requirement = utility.getPlanRequirment(plan_id)

    term_1 = utility.suggestion(possible_course, requirement, learned_course)

    for i in term_1:
        learned_course.append(utility.getCategory(i)[0])

    possible_course = utility.findPossibleCourse(learned_course, all_course)
    term_2 = utility.suggestion(
        possible_course, requirement, learned_course, term_id=2
    )

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
    term_2 = utility.suggestion(
        possible_course, requirement, learned_course, term_id=2
    )
    return {"term_1": term_1, "term_2": term_2}


@blueprint.route("/available_course", methods=["GET"])
@verify_session()
def avalable_course() -> dict:
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()
    student_id = utility.getStudentId(user_id)
    plan_id = utility.getPlanId(student_id)

    learned_course = utility.getUserEnrollment(student_id)
    all_course = utility.getCourse(plan_id)
    possible_course = utility.findPossibleCourse(learned_course, all_course)
    return {"course": possible_course}
