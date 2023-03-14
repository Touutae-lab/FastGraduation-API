import re
from typing import Any, Awaitable, Callable, Dict, List, Union

import config
import database
from supertokens_python.asyncio import delete_user
from supertokens_python.recipe.emailpassword import InputFormField
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface,
    APIOptions,
    SignUpPostEmailAlreadyExistsError,
    SignUpPostOkResult,
)
from supertokens_python.recipe.emailpassword.types import FormField
from supertokens_python.types import GeneralErrorResponse


def _validator(
    pattern: Union[str, re.Pattern[str]],
    invalid_msg: str,
    optional: bool = False,
) -> Callable[[str], Awaitable[Union[str, None]]]:
    async def wrapper(value: Any) -> Union[str, None]:
        if optional and value == "":
            return None
        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            return invalid_msg
        return None

    return wrapper


def _thai_validator(
    optional: bool = False,
) -> Callable[[str], Awaitable[Union[str, None]]]:
    return _validator(
        r"^[ก-๙]+$", "Invalid value; the field must be Thai.", optional
    )


def _eng_validator(
    optional: bool = False,
) -> Callable[[str], Awaitable[Union[str, None]]]:
    return _validator(
        r"^[A-Za-z-]+$", "Invalid value; the field must be English.", optional
    )


async def _student_id_validator(value: Any) -> Union[str, None]:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"^[0-9]{9}$", value) is None
    ):
        return "Invalid student ID format; it must be 9-digit value."

    cursor = database.db.cursor()
    database_name = config.config["mysql"]["database"]

    cursor.execute(
        (
            f"SELECT `student_id` "
            f"FROM `{database_name}`.`student` "
            f"WHERE `student_id` = %s"
        ),
        [value],
    )

    if cursor.fetchall():
        return "The student ID exists in the database."

    return None


signup_formfields: List[InputFormField] = [
    InputFormField(
        id="student_id",
        validate=_student_id_validator,
    ),
    InputFormField(id="fname_th", validate=_thai_validator()),
    InputFormField(
        id="mname_th", validate=_thai_validator(True), optional=True
    ),
    InputFormField(id="lname_th", validate=_thai_validator()),
    InputFormField(id="fname_en", validate=_eng_validator()),
    InputFormField(
        id="mname_en", validate=_eng_validator(True), optional=True
    ),
    InputFormField(id="lname_en", validate=_eng_validator()),
]


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

                if data_user["mname_en"] == "":
                    del data_user["mname_en"]
                if data_user["mname_th"] == "":
                    del data_user["mname_th"]

                data_user["user_id"] = user_id
                data_student["user_id"] = user_id

                data_user["type"] = 1
                data_student["academic_year"] = (
                    int("25" + data_student["student_id"][:2]) - 543
                )

                # Add to user table
                database.insert("user", data_user)
                # Add to student table
                database.insert("student", data_student)

            except Exception as e:
                # revert the action if user data are not complete
                await delete_user(user_id)
                raise e

        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation
