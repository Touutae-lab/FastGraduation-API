from typing import Any, Dict, Final, List, Tuple, Union

import config
import mysql.connector

_host = config.config["mysql"]["host"]
_port = config.config["mysql"]["port"]
_user = config.config["mysql"]["user"]
_password = config.config["mysql"]["password"]
_database = config.config["mysql"]["database"]


class Database:
    def __init__(self, host, port, user, password, database) -> None:
        self.conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )

    def delete(
        self,
        table: str,
        where: Union[Dict[str, Any], str],
        whereargs: Union[List[Any], None] = None,
        database: str = _database,
    ):
        """
        ::example::

        ```python
        import database


        delete("student", {"student_id": 630510600})
        ```
        """
        cursor = self.conn.cursor()

        where_str, valargs = _where_str(where, whereargs)
        status = cursor.execute(
            _QUERY["delete"]
            % {
                "database": database,
                "table": table,
                "where": where_str,
            },
            valargs,
        )
        self.conn.commit()

        return status

    def insert(
        self,
        table: str,
        data: Dict[str, Any],
        database: str = _database,
    ):
        """
        ::example::

        ```python
        import database


        insert(
            "student",
            {
                "user_id": "3fbed483-e7be-4d3d-8d20-c17c6c526794",
                "student_id": 630510600,
                "academic_year": 2020,
            }
        )
        ```
        """
        cursor = self.conn.cursor()

        colstr: str = ", ".join((f"`{col}`" for col in data.keys()))
        valf: str = ", ".join(["%s"] * len(data))

        status = cursor.execute(
            _QUERY["insert"]
            % {
                "database": database,
                "table": table,
                "colstr": colstr,
                "valf": valf,
            },
            tuple(data.values()),
        )
        self.conn.commit()

        return status

    def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: Union[Dict[str, Any], str],
        whereargs: Union[List[Any], None] = None,
        database: str = _database,
    ):
        """
        ::example::

        ```python
        import database


        update(
            "student",
            data={"academic_year": 2022},
            where={"student_id": 630510600}
        )
        ```
        """
        cursor = self.conn.cursor()
        valargs: List[Any] = []
        set_statements: str = ", ".join((f"{col} = %s" for col in data))
        valargs.extend(data.values())

        where_str, whereargs = _where_str(where, whereargs)
        if isinstance(where, dict):
            valargs.extend(list(where.values()))
        else:
            valargs.extend(whereargs)

        status = cursor.execute(
            _QUERY["update"]
            % {
                "database": database,
                "table": table,
                "set_statements": set_statements,
                "where": where_str,
            },
            valargs,
        )
        self.conn.commit()

        return status

    def execute(self, query, arguments, commit=False):
        """
        To directly execute custom SQL command, if necessary

        Note: for SELECT, please use this one

        ::example::

        To execute SELECT type FROM user WHERE username = [value]:
        ```python
        from database import db

        # assume that current_username is assigned elsewhere.
        db.update(
            query="SELECT type FROM user WHERE username = %s",
            arguments=[current_username]  # this maps to above %s
        )
        ```
        """
        cursor = self.conn.cursor()
        status = cursor.execute(query, arguments)
        if commit:
            self.conn.commit()

        return cursor, status


db_oop = Database(_host, _port, _user, _password, _database)

db = mysql.connector.connect(
    host=_host,
    port=_port,
    user=_user,
    password=_password,
    database=_database,
)


_QUERY: Final[Dict[str, str]] = {
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


def delete(
    table: str,
    where: Union[Dict[str, Any], str],
    whereargs: Union[List[Any], None] = None,
    database: str = config.config["mysql"]["database"],
):
    """
    ::example::

    ```python
    import database


    delete("student", {"student_id": 630510600})
    ```
    """
    cursor = db.cursor()

    where_str, valargs = _where_str(where, whereargs)
    status = cursor.execute(
        _QUERY["delete"]
        % {
            "database": database,
            "table": table,
            "where": where_str,
        },
        valargs,
    )
    db.commit()

    return status


def insert(
    table: str,
    data: Dict[str, Any],
    database: str = config.config["mysql"]["database"],
):
    """
    ::example::

    ```python
    import database


    insert(
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
        _QUERY["insert"]
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


    update(
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

    where_str, whereargs = _where_str(where, whereargs)

    if isinstance(where, dict):
        valargs.extend(list(where.values()))
    else:
        valargs.extend(whereargs)

    status = cursor.execute(
        _QUERY["update"]
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


def _where_str(
    where: Union[Dict[str, Any], str],
    whereargs: Union[List[Any], None] = None,
) -> Tuple[str, List[Any]]:

    where_str: str = (
        where
        if isinstance(where, str)
        else " AND ".join((f"{col} = %s" for col in where))
    )
    valargs: List[Any] = []

    if isinstance(where, dict):
        valargs.extend(list(where.values()))
    else:
        valargs.extend(whereargs)

    return where_str, valargs
