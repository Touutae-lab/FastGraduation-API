"""
Utility Functions
#################

"""
import random

from database import db


class EnrollmentDelegate:
    def __init__(self) -> None:
        self.cursor = db.cursor()

    def getStudentId(self, user_id: str) -> int:
        query: str = "SELECT student_id FROM student WHERE user_id = %s"
        cursor = db.cursor()
        cursor.execute(query, [user_id])

        result = cursor.fetchall()

        return result[0][0]

    def getPlanId(self, student_id: str) -> int:
        query: str = "SELECT academic_year FROM student WHERE student_id = %s"
        cursor = db.cursor()
        cursor.execute(query, [student_id])

        result = cursor.fetchall()[0][0]

        plan_id = 3
        if result == 2020:
            plan_id = 1

        return plan_id

    def getEnrollmentCourse(self, studentId: str) -> list:
        query: str = (
            "SELECT course_id, category_id FROM enrollment "
            "WHERE student_id = %s AND grade != 'F'"
        )
        cursor = db.cursor()
        cursor.execute(query, [studentId])

        result = cursor.fetchall()
        db.commit()

        return result

    def getCourse(self, course: int = 1) -> list:
        query: str = (
            "SELECT course_id FROM default_course_plan WHERE plan_id = %s"
        )
        cursor = db.cursor()
        cursor.execute(query, [course])

        data = cursor.fetchall()
        db.commit()

        result = []
        for i in data:
            result.append(i[0])
        return result

    def findPrerequisite(self, course):
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

    def findPossibleCourse(self, learnedCourse: list, allCourse: list):
        can_learn = []
        learnedCourse = self.normallize(learnedCourse)
        result = []
        for i in allCourse:
            if i not in learnedCourse:
                can_learn.append(i)
        for i in can_learn:
            if self.canLearn(i, learnedCourse):
                result.append(i)
        result = set(result)
        pseudo = self.removeCourse()
        for i in pseudo:
            result.discard(i)
        return list(result)

    def getPlanRequirment(self, course: int = 1) -> dict:
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
    def canLearn(self, course: str, learned_course):
        pre = self.findPrerequisite(course)

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

    def normallize(self, course):
        return [data[0] for data in course]

    def removeCourse(self):
        query: str = "SELECT * FROM pseudo_course"
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        db.commit()
        result = self.normallize(data)
        return result

    def normallize_requirement(self, possible_course):
        query: str = (
            "SELECT * FROM default_course_category WHERE course_id = %s"
        )
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

    def getCreditCourse(self, course):
        query: str = "SELECT id, credit FROM course where id = %s"
        cursor = db.cursor()

        cursor.execute(query, [course])
        data = cursor.fetchall()
        db.commit()

        return data[0][1]

    def normCred(self, learned_course):
        result = {}
        for i in learned_course:
            key = i[1]
            value = self.getCreditCourse(i[0])
            if key not in result:
                result.update({key: value})
            result.update({key: result[key] + value})

        return result

    def checkOpen(self, course):
        query: str = "SELECT term_1, term_2 FROM course where id = %s"
        cursor = db.cursor()

        cursor.execute(query, [course])
        data = cursor.fetchall()
        db.commit()

        return data

    def getCategory(self, course):
        query: str = (
            "SELECT * FROM `default_course_category` WHERE course_id = %s"
        )
        cursor = db.cursor()

        cursor.execute(query, [course])
        data = cursor.fetchall()
        db.commit()
        return data
