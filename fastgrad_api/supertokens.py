from typing import Any, Dict, List, Union

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
            pass
            # user_id: str = response.user.user_id
            # email: str = response.user.email
            # breakpoint()

        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation
