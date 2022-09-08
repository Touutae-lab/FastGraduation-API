import mysql.connector
from flask import Blueprint

from .config import config

test_blueprint: Blueprint = Blueprint("test_blueprint", __name__)


@test_blueprint.route("/course_info")
def course_info() -> str:
    db = mysql.connector.connect(
        host=config["mysql"]["host"],
        port=config["mysql"]["port"],
        user=config["mysql"]["user"],
        password=config["mysql"]["password"],
        database=config["mysql"]["database"],
    )

    cursor = db.cursor()
    cursor.execute("SELECT * FROM course")

    result = cursor.fetchall()

    return str(result)
