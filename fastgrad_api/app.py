"""
Getting Started
====================================

"""

# import test

import admin
import config
import student
from flask import Flask, abort, g, jsonify
from flask_cors import CORS
from supertokens import override_email_password_apis, signup_formfields
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.framework.flask import Middleware
from supertokens_python.recipe import emailpassword, session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.flask import verify_session

init(
    app_info=InputAppInfo(
        app_name="App",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        api_base_path="/auth",
        website_base_path="/auth",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri="http://supertokens:3567",
    ),
    framework="flask",
    recipe_list=[
        emailpassword.init(
            sign_up_feature=emailpassword.InputSignUpFeature(
                form_fields=signup_formfields
            ),
            override=emailpassword.InputOverrideConfig(
                apis=override_email_password_apis
            ),
        ),
        session.init(),  # initializes session features
    ],
)


app: Flask = Flask(__name__)

Middleware(app)
CORS(
    app=app,
    origins=config.config["origins"],
    supports_credentials=True,
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# ********** BLUEPRINT REGISTERING **********
app.register_blueprint(admin.blueprint, url_prefix="/admin")
app.register_blueprint(student.blueprint, url_prefix="/student")
# app.register_blueprint(test.blueprint, url_prefix="/test")

# This is required since if this is not there, then OPTIONS requests for
# the APIs exposed by the supertokens' Middleware will return a 404
@app.route("/", defaults={"u_path": ""})
@app.route("/<path:u_path>")
def catch_all(u_path: str):
    abort(404)


@app.route("/sessioninfo", methods=["GET"])  # type: ignore
@verify_session()
def get_session_info():
    session_ = g.supertokens
    return jsonify(
        {
            "sessionHandle": session_.get_handle(),
            "userId": session_.get_user_id(),
            "accessTokenPayload": session_.get_access_token_payload(),
        }
    )


@app.route("/update-jwt", methods=["POST"])
@verify_session()
def like_comment():
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()

    return user_id


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
