"""
app.py
====================================
The core module of the project.
"""
import core
from flask import Flask
from supertokens_python.recipe.session import SessionContainer
from supertokens_python import get_all_cors_headers
from flask import Flask, abort, g
from flask_cors import CORS 
from supertokens_python.framework.flask import Middleware
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session
from supertokens_python.recipe.session.framework.flask import verify_session
import os
import time
#from core import get_hit_count

init(
    app_info=InputAppInfo(
        app_name="App",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        api_base_path="/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        # try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
        connection_uri="https://try.supertokens.com",
        # api_key="IF YOU HAVE AN API KEY FOR THE CORE, ADD IT HERE"
    ),
    framework='flask',
    recipe_list=[
        session.init(), # initializes session features
        emailpassword.init()
    ]
)


app = Flask(__name__)
Middleware(app)

# TODO: Add APIs

CORS(
    app=app,
    origins=[
        "http://localhost:3000"
    ],
    supports_credentials=True,
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# This is required since if this is not there, then OPTIONS requests for
# the APIs exposed by the supertokens' Middleware will return a 404
@app.route('/', defaults={'u_path': ''})  
@app.route('/<path:u_path>')  
def catch_all(u_path: str):
    abort(404)

# def login():
#     core.login
#     """
#     Return the Session info
#     ----------
#     your_name
#         A string indicating the name of the person.
#     """
#     return "kuy"
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

# def login():
#     core.login
#     """
#     Return the most important thing about a person.
#     Parameters
#     ----------
#     your_name
#         A string indicating the name of the person.
#     """
#     return "kuy"
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

@app.route('/update-jwt', methods=['POST']) 
@verify_session()
def like_comment():
    session: SessionContainer = g.supertokens 

    user_id = session.get_user_id()

    print(user_id)
