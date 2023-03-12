from typing import List

from database import db_oop as db
from flask import Blueprint, request,g
from route import Route, register_route
from . import utility
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("missing_credits", __name__)



#student_id: str
class MissingCredits(Route):
    def __init__(self) -> None:
        super().__init__(path="/missing_credits", methods=["GET"])
    @verify_session()
    def get(self, *args, **kwargs):
        session: SessionContainer = g.supertokens
        user_id = session.get_user_id()
        student_id=utility.getStudentId(user_id)
        
        # student_id="630510501"
        count=1

        plan_id=utility.getPlanId(student_id) 
        all_credit=utility.getPlanRequirment(plan_id)
        credits=self.check_credits(student_id)
        for i in credits:
            if i != 0:
                all_credit[count]-=i
            count+=1

        msg=self.warning(all_credit)
        return {"status": "success",
        "msg": "OK",
        "data": [msg,all_credit]}

    def check_credits(self,student_id: str):
        credits=[0 for i in range(10)]
        enroll=utility.getUserEnrollment(student_id)
        for i in enroll:
            credits[i[1]-1] +=utility.getCreditCourse(i[0])
        return credits

    def warning(self,all_credit:dict)-> list:
        warning_msg={"no minor":"เนื่องจากคุณลงคอมเพียว หน่วยกิตของminorจะคิดเพิ่มไปไนวิชา300/400 ",
                     "over GE" : "คุณเรียนตัวGEมากกว่าที่หลักสูตรกำหนดไว้ หน่วยกิตGEที่เกินมาจะไปเพิ่มเป็นตีวฟรี",
                     "700":"เนื่องจากแผนการเรียน  หลักสูตรก้าวหน้า หลักสูตร64 จำเป็นต้องเรียนวิชา700"}
        msg=[]
        if all_credit[8] is  None:
              msg.append(warning_msg["no minor"])
        elif all_credit[1] >6:
              msg.append(warning_msg["over GE"])

        elif all_credit.get(9) is not None and all_credit[9] !=0:
              msg.append(warning_msg["700"])    
        return msg
_route: Route = MissingCredits()
register_route(blueprint, _route)