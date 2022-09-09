import config
import mysql.connector
from flask import Blueprint

test_blueprint: Blueprint = Blueprint("test_blueprint", __name__)


@test_blueprint.route("/course_info")
def course_info() -> str:
    db = mysql.connector.connect(
        host=config.config["mysql"]["host"],
        port=config.config["mysql"]["port"],
        user=config.config["mysql"]["user"],
        password=config.config["mysql"]["password"],
        database=config.config["mysql"]["database"],
    )

    cursor = db.cursor()
    cursor.execute("SELECT * FROM course")

    result = cursor.fetchall()

    return str(result)
