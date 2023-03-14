import asyncio

import database
from flask import Blueprint
from supertokens_python.recipe.session.framework.flask import verify_session

blueprint: Blueprint = Blueprint("sql_update", __name__)


@blueprint.route("/sql_update")
@verify_session()
def test_sql_update():
    async def wrapper():
        await database.update(
            table="student",
            data=dict(student_id=630510999),
            where=dict(student_id=630510600),
        )

    asyncio.gather(wrapper())

    return {"msg": "success"}
