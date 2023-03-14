import random

# from database import db_oop as db
from flask import Blueprint, g
from route import Route, register_route
from student.utility import EnrollmentDelegate
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("suggest", __name__)

rank: list = [5, 4, 3]

# class UserDefine:
#     self.data
#     self.naruto
#     self.dice
class Suggestion(Route):
    def __init__(self) -> None:
        super().__init__(path="/suggest", methods=["GET"])
        self.enroll = EnrollmentDelegate()

    @verify_session()
    def get(self, *args, **kwargs) -> dict:

        session: SessionContainer = g.supertokens
        user_id: str = session.get_user_id()

        student_id: str = self.enroll.getStudentId(user_id)
        plan_id: str = self.enroll.getPlanId(student_id)

        all_course = self.enroll.getCourse(plan_id)
        learned_course = self.enroll.getEnrollmentCourse(student_id)
        possible_course = self.enroll.findPossibleCourse(
            learned_course, all_course
        )
        requirement = self.enroll.getPlanRequirment(plan_id)

        term_1 = self.suggestion(possible_course, requirement, learned_course)

        for i in term_1:
            learned_course.append(self.enroll.getCategory(i)[0])

        possible_course = self.enroll.findPossibleCourse(
            learned_course, all_course
        )
        term_2 = self.suggestion(
            possible_course, requirement, learned_course, term_id=2
        )

        return {"term_1": term_1, "term_2": term_2}

    def suggestion(
        self,
        possiblecourse: list,
        requirement: dict,
        learned_course,
        term_id=1,
    ):
        norm_possible = self.enroll.normallize_requirement(possiblecourse)
        norm_cred = self.enroll.normCred(learned_course)

        for i in requirement:
            if i in norm_cred:
                requirement.update({i: requirement[i] - norm_cred[i]})

        need_learn = [i for i in requirement if requirement[i] != 0]

        result = []
        for i in norm_possible[5]:
            result.append(i)

        suggest = random.sample(result, 3)

        while len(suggest) < 8:
            c = random.sample(need_learn, 1)
            if int(c[0]) in norm_possible:
                token = random.sample(norm_possible[int(c[0])], 1)
                if token[0] not in suggest:
                    suggest.append(token[0])
            if term_id == 1:
                for i in suggest:
                    if self.enroll.checkOpen(i)[0][0] == 1:
                        pass
                    else:
                        suggest.remove(i)
            if term_id == 2:
                for i in suggest:
                    if self.enroll.checkOpen(i)[0][1] == 1:
                        pass
                    else:
                        suggest.remove(i)
        return suggest


# @blueprint.route("/suggest", methods=["GET"])
# @verify_session()
# def postSuggest() -> dict:
#     """_summary_
#     the request body must look like this
#     course: number
#     while number in range (1,6)
#     Returns:
#         _type_: _description_
#     """

#     session: SessionContainer = g.supertokens
#     user_id = session.get_user_id()
#     student_id = utility.getStudentId(user_id)
#     plan_id = utility.getPlanId(student_id)

#     all_course = utility.getCourse(plan_id)
#     learned_course = utility.getUserself.enrollment(student_id)
#     possible_course = utility.findPossibleCourse(learned_course, all_course)
#     requirement = utility.getPlanRequirment(plan_id)

#     term_1 = utility.suggestion(possible_course, requirement, learned_course)

#     for i in term_1:
#         learned_course.append(utility.getCategory(i)[0])

#     possible_course = utility.findPossibleCourse(learned_course, all_course)
#     term_2 = utility.suggestion(
#         possible_course, requirement, learned_course, term_id=2
#     )

#     return {"term_1": term_1, "term_2": term_2}


@blueprint.route("/trytotest", methods=["GET"])
async def testStudent() -> dict:
    learned_course = self.enroll.getUserself.enrollment("630510501")
    all_course = self.enroll.getCourse()
    possible_course = self.enroll.findPossibleCourse(
        learned_course, all_course
    )

    requirement = self.enroll.getPlanRequirment()
    term_1 = self.enroll.suggestion(
        possible_course, requirement, learned_course
    )
    for i in term_1:
        learned_course.append(self.enroll.getCategory(i)[0])

    possible_course = self.enroll.findPossibleCourse(
        learned_course, all_course
    )
    term_2 = self.enroll.suggestion(
        possible_course, requirement, learned_course, term_id=2
    )
    return {"term_1": term_1, "term_2": term_2}


@blueprint.route("/available_course", methods=["GET"])
@verify_session()
def avalable_course() -> dict:
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()
    student_id = self.enroll.getStudentId(user_id)
    plan_id = self.enroll.getPlanId(student_id)

    learned_course = self.enroll.getUserself.enrollment(student_id)
    all_course = self.enroll.getCourse(plan_id)
    possible_course = self.enroll.findPossibleCourse(
        learned_course, all_course
    )
    return {"course": possible_course}


_route: Route = Suggestion()

register_route(blueprint, _route)
