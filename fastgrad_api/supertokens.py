from datetime import datetime
from typing import Any, Dict, List, Union

import database
from supertokens_python.asyncio import delete_user
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface,
    APIOptions,
    SignUpPostEmailAlreadyExistsError,
    SignUpPostOkResult,
)
from supertokens_python.recipe.emailpassword.types import FormField
from supertokens_python.types import GeneralErrorResponse


def override_email_password_apis(
    original_implementation: APIInterface,
) -> APIInterface:
    original_sign_up_post = original_implementation.sign_up_post

    async def sign_up_post(
        form_fields: List[FormField],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ) -> Union[
        SignUpPostOkResult,
        SignUpPostEmailAlreadyExistsError,
        GeneralErrorResponse,
    ]:

        # First we call the original implementation of signInPOST.
        response: Union[
            SignUpPostOkResult,
            SignUpPostEmailAlreadyExistsError,
            GeneralErrorResponse,
        ] = await original_sign_up_post(form_fields, api_options, user_context)

        # Post sign up response, we check if it was successful
        if isinstance(response, SignUpPostOkResult):
            user_id: str = response.session.user_id
            data_user: Dict[str, Any] = {
                "email": None,
                "fname_en": None,
                "mname_en": None,
                "lname_en": None,
                "fname_th": None,
                "mname_th": None,
                "lname_th": None,
            }

            data_student: Dict[str, Any] = {
                "student_id": None,
            }

            try:
                for field in form_fields:
                    if field.id in data_user.keys():
                        data_user[field.id] = field.value
                    if field.id in data_student.keys():
                        data_student[field.id] = field.value

                # if data_user["mname_en"] == "":
                #     data_user["mname_en"] = None
                # if data_user["mname_th"] == "":
                #     data_user["mname_th"] = None

                data_user["user_id"] = user_id
                data_student["user_id"] = user_id

                data_user["type"] = 1
                data_student["academic_year"] = (
                    datetime.now().year
                    - int("25" + data_student["student_id"][:2])
                    - 542
                )

                # Add to user table
                await database.insert("user", data_user)
                # Add to student table
                await database.insert("student", data_student)

            except Exception as e:
                # revert the action if user data are not complete
                await delete_user(user_id)
                raise e

        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation
