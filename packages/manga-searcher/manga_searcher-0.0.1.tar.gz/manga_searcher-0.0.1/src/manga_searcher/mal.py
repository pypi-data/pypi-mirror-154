# Typing.
from __future__ import annotations
from typing import Union

# For creating enums.
from enum import Enum

# For opening gzipped MAL mangalist.
import gzip

# For typing.
from io import TextIOWrapper

# For storing MAL manga list to database.
import sqlite3

# For getting file extension.
from pathlib import Path

# For parsing MAL mangalist XML-file
from xml.etree import ElementTree

# For handeling database.
from .db import Database, Table

# For downloading MyAnimeList.
from myanimelist_downloader.downloader import Downloader, List, Credentials, Dir


class Status(Enum):
    """MAL status"""

    NONE = None
    COMPLETED = 0
    ON_HOLD = 1
    PLAN_TO_READ = 2
    DROPPED = 3
    READING = 4

    # XML to Status mapping.
    __MAPPING__ = {
        "Completed": COMPLETED,
        "On-Hold": ON_HOLD,
        "Plan to Read": PLAN_TO_READ,
        "Dropped": DROPPED,
        "Reading": READING,
    }

    def from_mal(status: str) -> Status:
        return Status(Status.__MAPPING__[status])


class Manga(Table):
    """Object to store MAL manga."""

    # MAL id.
    id: int

    # Read volumes count.
    volumes: int = 0

    # Read chapters count.
    chapters: int = 0

    # Reading status.
    status: Status

    DB_TABLE: str = "mal_manga"
    DB_FIELDS: dict[str, str] = {
        "id": "INT UNSIGNED NOT NULL PRIMARY KEY",
        "volumes": "TINYINT UNSIGNED UNSIGNED NOT NULL DEFAULT 0",
        "chapters": "SMALLINT UNSIGNED UNSIGNED NOT NULL DEFAULT 0",
        "status": "TINYINT UNSIGNED NOT NULL",
    }

    def __init__(
        self: Manga,
        id: Union[int, None] = None,
        volumes: Union[int, None] = None,
        chapters: Union[int, None] = None,
        status: Union[Status, None] = None,
        xml: ElementTree.Element = None,
        row: sqlite3.Row = None,
    ):
        """Initialize MAL Manga object.

        Args:
            id (Union[int, None], optional): MAL id. Defaults to None.
            volumes (Union[int, None], optional): Read volumes count. Defaults to None.
            chapters (Union[int, None], optional): Read chapters count. Defaults to None.
            status (Union[Status, None], optional): Reading status. Defaults to None.
            xml (xml.etree.ElementTree.Element, optional): XML element to read from. Defaults to None.
            row (sqlite3.Row, optional): Database row to read from. Defaults to None.
        """

        # Get id.
        if id is not None:
            self.id = id
        elif xml:
            self.id = int(xml.find("manga_mangadb_id").text)
        else:
            self.id = row["id"]

        # Get volumes.
        if volumes is not None:
            self.volumes = volumes
        elif xml:
            self.volumes = int(xml.find("my_read_volumes").text)
        else:
            self.volumes = row["volumes"]

        # Get chapters.
        if chapters is not None:
            self.chapters = chapters
        elif xml:
            self.chapters = int(xml.find("my_read_chapters").text)
        else:
            self.chapters = row["chapters"]

        # Get status.
        if status is not None:
            self.status = status
        elif xml:
            self.status = Status.from_mal(xml.find("my_status").text)
        else:
            self.status = Status(row["status"])

    def insert_tuple(self: Manga) -> tuple:
        """Get SQL insert tuple.

        Returns:
            tuple: SQL insert tuple.
        """
        return (
            self.id,
            self.volumes,
            self.chapters,
            self.status.value,
        )

    def url(self: Manga) -> str:
        """MAL url.

        Returns:
            str: MAL url.
        """
        return "https://myanimelist.net/manga/{id}/".format(id=self.id)

    @classmethod
    def download_list(cls, data_directory: Dir) -> str:
        """Download manga list from MAL

        Returns:
            str: Path to downloaded manga list.
        """

        # Generate temporaty downloads directory.
        dir_downloads = Dir("mal_lists", data_directory)
        # Clear downloads directory.
        dir_downloads.clear()

        return (
            Downloader(
                credentials=Credentials.get(service="MAL"),
                download_directory=dir_downloads,
            )
        ).download_list(list=List.MANGA)

    @classmethod
    def generate_list(
        cls,
        db: Database,
        data_directory: Dir,
        file: Union[TextIOWrapper, None] = None,
        download=False,
    ) -> dict[int, Manga]:
        # Create manga table if not exists.
        cursor = cls.create(db=db)

        # Set file to downloaded list, if asked to download and no file given.
        if download and file is None:
            file = open(cls.download_list(data_directory=data_directory), "r")

        # Mangalist file given.
        if file is not None:
            print("Updating MAL list...")
            # Init insert list.
            mal_list: list[tuple] = []

            # Open file.
            with file as open_file:
                filepath: str = open_file.name
                suffix: str = Path(filepath).suffix
                # Handle .gz file.
                if suffix == ".gz":
                    with gzip.open(filepath, "rb") as gzipped_file:
                        tree = ElementTree.parse(gzipped_file)
                        del gzipped_file
                # Handle XML-file
                elif suffix == ".xml":
                    tree = ElementTree.parse(open_file)
                else:
                    raise Exception(
                        "Given mangalist file {filepath} was not .gz or .xml file!".format(
                            filepath=filepath
                        )
                    )
                del open_file, filepath, suffix

                # Add all Manga to list.
                manga: ElementTree.Element
                for manga in tree.getroot().findall("manga"):
                    mal_list.append(Manga(xml=manga).insert_tuple())
                del tree, manga

            # Delete all rows.
            cls.clear(db=db, cursor=cursor)
            cls.insert(db=db, cursor=cursor, rows=mal_list)
            del mal_list
            print("MAL list updated!")

        # Get MAL dictonary from database.
        return cls.db_list(db=db, cursor=cursor)
