import config
import mysql.connector

db = mysql.connector.connect(
    host=config.config["mysql"]["host"],
    port=config.config["mysql"]["port"],
    user=config.config["mysql"]["user"],
    password=config.config["mysql"]["password"],
    database=config.config["mysql"]["database"],
)

if __name__ == "__main__":
    print("This is the file just for database object.")
