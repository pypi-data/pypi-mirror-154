# Typing.
from __future__ import annotations
from typing import Any, Union

# For making database connection.
from sqlite3 import connect, Connection, Cursor, Row

# For handeling abstract Table class.
from abc import ABCMeta, abstractmethod


class Database:
    """Connect to database"""

    # Database connection.
    __con: Union[None, Connection] = None

    # Path to database file.
    __database_path: str

    def __init__(self: Database, database_path: str) -> None:
        """Initialize database.

        Args:
            self (Database): Itself.
            database_path (str): Path to database file.
        """

        self.__database_path = database_path

    def connect(self: Database) -> Connection:
        """Connect to database.

        Args:
            self (Database): Itself.

        Returns:
            Connection: Connection.
        """
        if self.__con is None:
            # Connect to database.
            self.__con = connect(self.__database_path)
            # Set rows to return sqlite3.Row element.
            self.__con.row_factory = Row
        return self.__con

    def cursor(self: Database, cursor: Union[Cursor, None] = None) -> Cursor:
        """Cursor to database.

        Args:
            self (Database): Itself.

        Returns:
            Cursor: Cursor to database.
        """
        return cursor or self.connect().cursor()

    def disconnect(self: Database) -> None:
        """Disconnect from database.

        Args:
            self (Database): Itself.
        """
        if self.__con is None:
            return
        self.__con.close()
        self.__con = None

    def table_create(
        self: Database,
        table: str,
        fields: dict[str, str],
        cursor: Union[Cursor, None] = None,
    ) -> Cursor:
        """Create database table.

        Args:
            self (Database): Itself.
            table (str): Tablename.
            fields (dict[str, str]): Field names and definitions.
            cursor (Union[Cursor, None]): If wanted to use specific cursor.
        Returns:
            Cursor: Used cursor.
        """

        cursor: Cursor = self.cursor(cursor)
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS
    `{table}`
(
    {fields}
);
""".format(
                table=table,
                fields=",\n".join(
                    [
                        "`{field_name}` {field_type}".format(
                            field_name=field_name, field_type=field_type
                        )
                        for field_name, field_type in fields.items()
                    ]
                ),
            )
        )
        return cursor

    def table_empty(
        self: Database, table: str, cursor: Union[Cursor, None] = None
    ) -> bool:
        """Is table empty?

        Args:
            self (Database): Itself.
            table (str): Tablename.
            cursor (Union[Cursor, None]): If wanted to use specific cursor.
        Returns:
            bool: Was table empty?
        """

        return (
            len(
                self.cursor(cursor)
                .execute("SELECT 1 FROM `{table}` LIMIT 1;".format(table=table))
                .fetchall()
            )
            == 0
        )

    def table_clear(
        self: Database, table: str, cursor: Union[Cursor, None] = None
    ) -> Cursor:
        """Clear database table.

        Args:
            self (Database): Itself.
            table (str): Tablename.
            cursor (Union[Cursor, None]): If wanted to use specific cursor.
        Returns:
            Cursor: Used cursor.
        """

        cursor: Cursor = self.cursor(cursor)
        cursor.execute("DELETE FROM `{table}`;".format(table=table))
        cursor.connection.commit()
        return cursor

    def table_insert(
        self: Database,
        table: str,
        fields: list[str],
        rows: list[tuple],
        cursor: Union[Cursor, None] = None,
    ) -> Cursor:
        """Insert to database table.

        Args:
            self (Database): Itself.
            table (str): Tablename.
            fields (list[str]): Field names.
            rows (list[tuple]): Rows to insert.
            cursor (Union[Cursor, None]): If wanted to use specific cursor.
        Returns:
            Cursor: Used cursor.
        """

        cursor: Cursor = self.cursor(cursor)
        cursor.executemany(
            "INSERT INTO `{table}` ({fields}) VALUES ({values})".format(
                table=table,
                fields=", ".join(
                    map(lambda field: "`{field}`".format(field=field), fields)
                ),
                values=", ".join(["?"] * len(fields)),
            ),
            rows,
        )
        cursor.connection.commit()
        return cursor


class Table(metaclass=ABCMeta):
    """Abstract class to handle database table."""

    @property
    @abstractmethod
    def DB_TABLE(self) -> str:
        """Database table name.

        Returns:
            str: Database table name.
        """

        pass

    @property
    @abstractmethod
    def DB_FIELDS(self) -> dict[str, str]:
        """Database field names to their definitions.

        Returns:
            dict[str, str]: Database field names to their definitions.
        """

        pass

    @abstractmethod
    def insert_tuple(self) -> tuple:
        """Tuple for inserting database row.

        Returns:
            tuple: Tuple for inserting database row.
        """

        pass

    @classmethod
    def create(
        cls, db: Union[Database, None] = None, cursor: Union[Cursor, None] = None
    ) -> Cursor:
        """Create database table.

        Args:
            db (Union[Database, None], optional): If wanted to use specific Database-object. Defaults to None.
            cursor (Union[Cursor, None], optional): If wanted to use specific Cursor-object. Defaults to None.

        Returns:
            Cursor: Used cursor.
        """

        return (db or Database()).table_create(
            table=cls.DB_TABLE, fields=cls.DB_FIELDS, cursor=cursor
        )

    @classmethod
    def clear(
        cls, db: Union[Database, None] = None, cursor: Union[Cursor, None] = None
    ) -> Cursor:
        """Clear database table.

        Args:
            db (Union[Database, None], optional): If wanted to use specific Database-object. Defaults to None.
            cursor (Union[Cursor, None], optional): If wanted to use specific Cursor-object. Defaults to None.

        Returns:
            Cursor: Used cursor.
        """

        return (db or Database()).table_clear(table=cls.DB_TABLE, cursor=cursor)

    @classmethod
    def empty(
        cls, db: Union[Database, None] = None, cursor: Union[Cursor, None] = None
    ) -> bool:
        """Is database table empty?

        Args:
            db (Union[Database, None], optional): If wanted to use specific Database-object. Defaults to None.
            cursor (Union[Cursor, None], optional): If wanted to use specific Cursor-object. Defaults to None.

        Returns:
            bool: Was database table empty?
        """

        return (db or Database()).table_empty(table=cls.DB_TABLE, cursor=cursor)

    @classmethod
    def insert(
        cls,
        rows: list[tuple],
        db: Union[Database, None] = None,
        cursor: Union[Cursor, None] = None,
    ) -> Cursor:
        """Insert rows to database table.

        Args:
            rows (list[tuple]): Rows to insert.
            db (Union[Database, None], optional): If wanted to use specific Database-object. Defaults to None.
            cursor (Union[Cursor, None], optional): If wanted to use specific Cursor-object. Defaults to None.

        Returns:
            Cursor: Used cursor.
        """
        return (db or Database()).table_insert(
            table=cls.DB_TABLE,
            fields=list(cls.DB_FIELDS),
            rows=rows,
            cursor=cursor,
        )

    @classmethod
    def db_list(
        cls,
        db: Union[Database, None] = None,
        cursor: Union[Cursor, None] = None,
    ) -> dict[Any, Table]:
        """Get objects from database table.

        Args:
            db (Union[Database, None], optional): If wanted to use specific Database-object. Defaults to None.
            cursor (Union[Cursor, None], optional): If wanted to use specific Cursor-object. Defaults to None.

        Returns:
            dict[Any, Table]: Dictornary of ids as keys and object as values.
        """

        # Init MAL dictonary.
        db_list: dict[Any, cls] = {}

        # Fill MAL dictonary from database.
        row: Row
        for row in (
            (db or Database())
            .cursor(cursor=cursor)
            .execute(
                "SELECT * FROM `{table}` ORDER BY `id` ASC".format(table=cls.DB_TABLE)
            )
        ):
            obj: cls = cls(row=row)
            del row
            db_list[obj.id] = obj
            del obj
        return db_list
