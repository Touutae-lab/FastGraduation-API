"""
Utility Functions
#################

"""
import random

from database import db


def getUserEnrollment(studentId: str) -> list:
    query: str = (
        "SELECT course_id, category_id FROM enrollment "
        "WHERE student_id = %s AND grade != 'F'"
    )
    cursor = db.cursor()
    cursor.execute(query, [studentId])

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


def findPrerequisite(course):
    query: str = "SELECT precourse_id, pregroup_id FROM `prerequisite` WHERE course_id = %s"
    cursor = db.cursor()
    cursor.execute(query, [course])

    data = cursor.fetchall()
    db.commit()

    result = {}

    if len(data) == 1:
        return data

    for i in data:
        if i[1] not in result:
            result.update({i[1]: [i[0]]})
        elif i[1] in result:
            result[i[1]].append(i[0])
    return result


def findPossibleCourse(learnedCourse: list, allCourse: list):
    can_learn = []
    learnedCourse = normallize(learnedCourse)
    result = []
    for i in allCourse:
        if i not in learnedCourse:
            can_learn.append(i)
    for i in can_learn:
        if canLearn(i, learnedCourse):
            result.append(i)
    result = set(result)
    pseudo = removeCourse()
    for i in pseudo:
        result.discard(i)
    return list(result)


def suggestion(
    possiblecourse: list, requirement: dict, learned_course, term_id=1
):
    norm_possible = normallize_requirement(possiblecourse)
    norm_cred = normCred(learned_course)

    for i in requirement:
        if i in norm_cred:
            requirement.update({i: requirement[i] - norm_cred[i]})

    need_learn = [i for i in requirement if requirement[i] != 0]

    result = []
    for i in norm_possible[5]:
        result.append(i)

    suggest = random.sample(result, 3)

    # c = random.sample(need_learn, 4)

    # for i in c:
    #     if i not in norm_possible:
    #         pass
    #     else:
    #         token = random.sample(norm_possible[int(i)], 1)
    #         if token[0] not in suggest:
    #             suggest.append(token[0])
    while len(suggest) < 8:
        c = random.sample(need_learn, 1)
        if int(c[0]) in norm_possible:
            token = random.sample(norm_possible[int(c[0])], 1)
            if token[0] not in suggest:
                suggest.append(token[0])
        if term_id == 1:
            for i in suggest:
                if checkOpen(i)[0][0] == 1:
                    pass
                else:
                    suggest.remove(i)
        if term_id == 2:
            for i in suggest:
                if checkOpen(i)[0][1] == 1:
                    pass
                else:
                    suggest.remove(i)
    return suggest


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
        result.update({couple[0]: couple[1]})

    return result


# Due the DB confusion this is the result for suggestion code LUL
def canLearn(course: str, learned_course):
    pre = findPrerequisite(course)

    query: str = (
        "SELECT inclusion_type FROM prerequisite_group WHERE group_no = %s"
    )
    cursor = db.cursor()

    if len(pre) == 0:
        return True

    if len(pre) == 1:
        if pre[0][0] in learned_course:
            return True
        else:
            return False

    for i in pre:
        cursor.execute(query, [i])
        data = cursor.fetchall()
        db.commit()

        if data[0][0] == "any":
            for j in pre[i]:
                if j in learned_course:
                    return True
        if data[0][0] == "all":
            count = 0
            for j in pre[i]:
                if j in learned_course:
                    count += 1
            if len(pre[i]) == count:
                return True
    return False


def normallize(course):
    return [data[0] for data in course]


def removeCourse():
    query: str = "SELECT * FROM pseudo_course"
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.commit()
    result = normallize(data)
    return result


def normallize_requirement(possible_course):
    query: str = "SELECT * FROM default_course_category WHERE course_id = %s"
    cursor = db.cursor()

    result = {}
    for i in possible_course:
        cursor.execute(query, [i])
        data = cursor.fetchall()
        db.commit()

        if data[0][1] not in result:
            result.update({data[0][1]: [data[0][0]]})
        elif data[0][1] in result:
            result[data[0][1]].append(data[0][0])
    return result

    """_summary_
    "course_category_id" : ""
    """


def getCreditCourse(course):
    query: str = "SELECT id, credit FROM course where id = %s"
    cursor = db.cursor()

    cursor.execute(query, [course])
    data = cursor.fetchall()
    db.commit()

    return data[0][1]


def normCred(learned_course):
    result = {}
    for i in learned_course:
        key = i[1]
        value = getCreditCourse(i[0])
        if key not in result:
            result.update({key: value})
        result.update({key: result[key] + value})

    return result


def checkOpen(course):
    query: str = "SELECT term_1, term_2 FROM course where id = %s"
    cursor = db.cursor()

    cursor.execute(query, [course])
    data = cursor.fetchall()
    db.commit()

    return data


def getCategory(course):
    query: str = "SELECT * FROM `default_course_category` WHERE course_id = %s"
    cursor = db.cursor()

    cursor.execute(query, [course])
    data = cursor.fetchall()
    db.commit()
    return data
