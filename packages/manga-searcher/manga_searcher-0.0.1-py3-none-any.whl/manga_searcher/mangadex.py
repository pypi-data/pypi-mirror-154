# Typing.
from __future__ import annotations
from sqlite3 import Row
from typing import Union

# Get username and password from user.
from myanimelist_downloader.downloader import Credentials

# For creating enums.
from enum import Enum

# API for MangaDex.
# https://api.mangadex.org/docs.html
# https://pypi.org/project/mangadex/
from mangadex import Api

# For connecting to database.
from .db import Database, Table


class Status(Enum):
    """MAL status"""

    NONE = None
    COMPLETED = 0
    ON_HOLD = 1
    PLAN_TO_READ = 2
    DROPPED = 3
    READING = 4
    RE_READING = 5

    __MAPPING__ = {
        "reading": READING,
        "on_hold": ON_HOLD,
        "plan_to_read": PLAN_TO_READ,
        "dropped": DROPPED,
        "re_reading": RE_READING,
        "completed": COMPLETED,
    }

    def from_api(status: str) -> Status:
        """From API-value to Status enum.

        Args:
            status (str): API-value.

        Returns:
            Status: Status enum.
        """

        return Status(Status.__MAPPING__[status])


class MangaDex(Api):
    """Wrapper for MangaDex API."""

    # Is logged in?
    __logged_in: bool = False

    def __init__(self):
        """Initialize."""
        super().__init__()

    def login_if_needed(self: MangaDex) -> MangaDex:
        """Login if needed.

        Args:
            self (MangaDex): Itself.

        Returns:
            MangaDex: Itself.
        """
        if not self.__logged_in:
            self.login()
        return self

    def login(self: MangaDex) -> MangaDex:
        """Login.

        Args:
            self (MangaDex): Itself.

        Returns:
            MangaDex: Itself.
        """

        credentials = Credentials.get("MANGA_DEX")
        Api.login(
            self,
            username=credentials.username,
            password=credentials.password,
        )

        self.__logged_in = True

    def status(
        self: MangaDex, db: Database, force_load: bool = False
    ) -> dict[str, Manga]:
        """Get manga reading statuses.

        Args:
            self (MangaDex): Itself
            force_load (bool, optional): Force load from API-even if already loaded. Defaults to False.

        Returns:
            dict[str, Manga]: Dictonary of Manga objects with ids as keys.
        """

        # Connect to MAL-mangalist database and get cursor.
        cursor = Manga.create(db=db)

        # If asked to force loading or no data in database.
        if force_load or Manga.empty(db=db, cursor=cursor):
            print("Updating MangaDex list...")
            # Get from database.
            mangas: list[tuple] = []
            id: str
            status: str
            for id, status in (
                self.login_if_needed().get_all_manga_reading_status().items()
            ):
                mangas.append(Manga(id, status=Status.from_api(status)).insert_tuple())
                del id, status

            # Clear
            Manga.clear(db=db, cursor=cursor)
            # and insert to table.
            Manga.insert(rows=mangas, db=db, cursor=cursor)
            del mangas
            print("MangaDex list updated!")

        # Get MangaDex manga dictonary from database.
        return Manga.db_list(db=db, cursor=cursor)


class Manga(Table):
    """MangaDex manga data object"""

    # Fields
    id: str
    status: Status

    # Database configuration.
    DB_TABLE: str = "manga_dex_manga"
    DB_FIELDS: dict[str, str] = {
        "id": "VARCHAR NOT NULL PRIMARY KEY",
        "status": "TINYINT UNSIGNED NOT NULL",
    }

    def __init__(
        self: Manga,
        id: Union[str, None] = None,
        status: Union[Status, None] = None,
        row: Row = None,
    ):
        """Initialize Mangadex Manga object.

        Args:
            id (Union[str, None], optional): MangaDex id. Defaults to None.
            status (Union[Status, None], optional): Reading status. Defaults to None.
            row (sqlite3.Row, optional): Database row to read from. Defaults to None.
        """

        # Get id.
        if id is not None:
            self.id = id
        else:
            self.id = row["id"]

        # Get status.
        if status is not None:
            self.status = status
        else:
            self.status = Status(row["status"])

    def insert_tuple(self: Manga) -> tuple:
        """Get SQL insert tuple.

        Returns:
            tuple: SQL insert tuple.
        """
        return (
            self.id,
            self.status.value,
        )

    def url(self: Manga) -> str:
        """MangaDex url.

        Returns:
            str: MAL url.
        """
        return "https://mangadex.org/title/{id}/".format(id=self.id)
