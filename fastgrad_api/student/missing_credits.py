from typing import List

from database import db_oop as db
from flask import Blueprint, g, request
from route import Route, register_route
from student.utility import EnrollmentDelegate
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("missing_credits", __name__)



#student_id: str
class MissingCredits(Route):
    def __init__(self) -> None:
        super().__init__(path="/missing_credits", methods=["GET"])
        
        self.enroll = EnrollmentDelegate()

    @verify_session()
    def get(self, *args, **kwargs):
        session: SessionContainer = g.supertokens
        user_id = session.get_user_id()
        student_id= self.enroll.getStudentId(user_id)
        
        # student_id="630510501"
        count=1

        plan_id=self.enroll.getPlanId(student_id) 
        all_credit=self.enroll.getPlanRequirment(plan_id)
        credits=self.check_credits(student_id)
        for i in credits:
            if i != 0:
                all_credit[count]-=i
            count+=1
        info = self.info(all_credit,student_id)
        msg = self.warning(all_credit)
        
        return {"status": "success",
        "msg": "OK",
        "data": [info,msg,all_credit]}

    def check_credits(self,student_id: str):
        credits=[0 for i in range(10)]
        enrollUser=self.enroll.getEnrollmentCourse(student_id)
        for i in enrollUser:
            credits[i[1]-1] += self.enroll.getCreditCourse(i[0])
        return credits

    def warning(self,all_credit:dict)-> list:
        warning_msg={"no minor":"เนื่องจากคุณลงคอมเพียว หน่วยกิตของminorจะคิดเพิ่มไปไนวิชา300/400 ",
                     "over GE" : "คุณเรียนตัวGEมากกว่าที่หลักสูตรกำหนดไว้ หน่วยกิตGEที่เกินมาจะไปเพิ่มเป็นตีวฟรี",
                     "700":"เนื่องจากแผนการเรียน  หลักสูตรก้าวหน้า หลักสูตร64 จำเป็นต้องเรียนวิชา700"}
        msg=[]
        if all_credit[8] ==0:
              msg.append(warning_msg["no minor"])
        elif all_credit[1] >6:
              msg.append(warning_msg["over GE"])

        elif all_credit.get(9) is not None and all_credit[9] !=0:
              msg.append(warning_msg["700"])    
        return msg
    
    def info(self,all_credit,student_id:dict):
        warning_msg={"no minor":"เพียวคอม",
                      "minor":"โทอื่น"}
        msg=[]
        planid=self.enroll.getPlanId(student_id) 
        if all_credit[8] ==0:
            msg.append(warning_msg["no minor"])
        elif all_credit[8] !=0:
            msg.append(warning_msg["minor"])

        if planid == 1:
            msg.append("แผนปกติ")
        elif planid == 3:
            msg.append("แผนปกติ64")
        return msg
    
_route: Route = MissingCredits()
register_route(blueprint, _route)