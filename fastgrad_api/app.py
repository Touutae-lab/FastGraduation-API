"""
app.py
====================================
The core module of the project.
"""
import course
from config import config
from flask import Flask, abort, g, jsonify
from flask_cors import CORS
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
        session.init(),  # initializes session features
        emailpassword.init(),
    ],
)


app: Flask = Flask(__name__)
Middleware(app)


CORS(
    app=app,
    origins=config["origins"],
    supports_credentials=True,
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# This is required since if this is not there, then OPTIONS requests for
# the APIs exposed by the supertokens' Middleware will return a 404
@app.route("/", defaults={"u_path": ""})
@app.route("/<path:u_path>")
def catch_all(u_path: str):
    abort(404)


# TODO: Add API Routes


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


@app.route("/hee")
def hee():
    """
    Return the most important thing about a person.
    Parameters
    ----------
    your_name
        A string indicating the name of the person.
    """
    return "CMU SO FUN"


@app.route("/update-jwt", methods=["POST"])
@verify_session()
def like_comment():
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()

    return user_id


app.register_blueprint(course.test_blueprint)
