from database import db


def getUserEnrollment(studentId: str) -> list:
    query: str = f"""SELECT course_id, category_id FROM enrollment
    WHERE student_id = %d"""
    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    db.commit()
    return result


def getCourse(course: int = 1) -> list:
    query: str = "SELECT course_id FROM default_course_plan WHERE plan_id = %s"
    cursor = db.cursor()
    cursor.execute(query, [course])

    data = cursor.fetchall()
    db.commit()

    result = []
    for i in data:
        result.append(i[0])
    return result


def findPrerequisite(course: dict):
    return


def findPostrequisite():
    return


def findPossibleCourse(learnedCourse: list, allCourse: list):
    can_learn = []
    not_decide = []
    for value in allCourse:
        if value not in learnedCourse:
            not_decide.append(value)
    for value in not_decide:
        if not_decide:
            can_learn.append(value)

    return can_learn


def suggestion(Possiblecourse: dict, requirement: dict):
    return


def getPlanRequirment(course: int = 1) -> dict:
    query: str = "SELECT category_id, min_credit FROM plan_requirement WHERE plan_id = {:}".format(
        course
    )

    cursor = db.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    db.commit()

    result = {}
    for couple in data:
        result.update({couple[0]: [couple[1]]})

    return result
