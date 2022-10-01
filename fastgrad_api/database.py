from typing import Any, Dict, Final, List, Union

import config
import mysql.connector

db = mysql.connector.connect(
    host=config.config["mysql"]["host"],
    port=config.config["mysql"]["port"],
    user=config.config["mysql"]["user"],
    password=config.config["mysql"]["password"],
    database=config.config["mysql"]["database"],
)

QUERY: Final[Dict[str, str]] = {
    "insert": (
        "INSERT INTO `%(database)s`.`%(table)s` "
        "(%(colstr)s) "
        "VALUES (%(valf)s)"
    ),
    "select": (
        "SELECT %(cols)s "
        "FROM `%(database)s`.`%(table)s` "
        "%(join_statement)s "
        "%(where)s "
        "%(groupby)s "
        "%(having)s "
        "%(orderby)s "
        "%(limit)s"
    ),
    "update": (
        "UPDATE `%(database)s`.`%(table)s` "
        "SET %(set_statements)s "
        "WHERE %(where)s"
    ),
    "delete": ("DELETE FROM `%(database)s`.`%(table)s` " "WHERE %(where)s"),
}


def insert(
    table: str,
    data: Dict[str, Any],
    database: str = config.config["mysql"]["database"],
):
    """
    ::example::

    ```python
    import database


    await insert(
        "student",
        {
            "user_id": "3fbed483-e7be-4d3d-8d20-c17c6c526794",
            "student_id": 630510600,
            "academic_year": 2020,
        }
    )
    ```
    """
    cursor = db.cursor()

    colstr: str = ", ".join((f"`{col}`" for col in data.keys()))
    valf: str = ", ".join(["%s"] * len(data))

    status = cursor.execute(
        QUERY["insert"]
        % {
            "database": database,
            "table": table,
            "colstr": colstr,
            "valf": valf,
        },
        tuple(data.values()),
    )
    db.commit()

    return status


def update(
    table: str,
    data: Dict[str, Any],
    where: Union[Dict[str, Any], str],
    whereargs: Union[List[Any], None] = None,
    database: str = config.config["mysql"]["database"],
):
    """
    ::example::

    ```python
    import database


    await update(
        "student",
        data={"academic_year": 2022},
        where={"student_id": 630510600}
    )
    ```
    """
    cursor = db.cursor()

    valargs: List[Any] = []

    set_statements: str = ", ".join((f"{col} = %s" for col in data))
    valargs.extend(data.values())

    where_str: str = (
        where
        if isinstance(where, str)
        else " AND ".join((f"{col} = %s" for col in where))
    )

    print(
        QUERY["update"]
        % {
            "database": database,
            "table": table,
            "set_statements": set_statements,
            "where": where_str,
        }
    )
    if isinstance(where, dict):
        valargs.extend(list(where.values()))
    else:
        valargs.extend(whereargs)

    status = cursor.execute(
        QUERY["update"]
        % {
            "database": database,
            "table": table,
            "set_statements": set_statements,
            "where": where_str,
        },
        valargs,
    )
    db.commit()

    return status


if __name__ == "__main__":
    print("This is the file just for database object.")
