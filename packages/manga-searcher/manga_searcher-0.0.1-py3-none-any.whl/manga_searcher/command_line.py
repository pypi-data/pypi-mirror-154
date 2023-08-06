# Typing.
from typing import List, Dict, Union


# API for mangaupdates.com.
# https://py-manga.readthedocs.io/en/latest/
from pymanga import series

# Get current working directory for default arguments.
from os import getcwd

# From os.path get directory and file check and path joiner.
from os.path import isdir, isfile, join

# Argument parsing.
from argparse import ArgumentParser, Namespace, FileType, BooleanOptionalAction
from typedate import TypeDate

# Handle .env files.
from dotenv import load_dotenv

# For opening browser tabs.
from .browser import web_open_tab
from .db import Database

# For storing variables.
from .storage import store

# For handeling MAL manga list.
from .mal import Manga as MALManga, Status as MALStatus

# MangaDex API and database classes.
from .mangadex import MangaDex, Status as MangaDexStatus, Manga as MangaDexManga
from mangadex import Tag, Chapter

# For transforming chapter float count to integer.
from math import floor

# For writing JSON-data.
import json

# For handeling directories.
from myanimelist_downloader.downloader import Dir

# For generating random string for output filenames.
from random import choices
from string import ascii_lowercase

# For getting current time.
from time import strftime


def main():

    # Working directory.
    working_directory: str = getcwd()

    # Load .env file.
    default_env_path: str = join(working_directory, ".env")
    if isfile(default_env_path):
        load_dotenv(dotenv_path=default_env_path)
    del default_env_path

    # Generate MangaDex API.
    api = MangaDex()

    # Get tags.
    tags: List[Tag] = store(
        data_directory=Dir("manga_searcher_tmp", working_directory),
        key="tags",
        value=api.tag_list,
    )

    # Generate tag titles list
    tag_titles: List[str] = []
    # and tag to id dictonary.
    tag_to_id: dict[str, str] = {}
    tag: Tag
    for tag in tags:
        tag_title = tag.name["en"]
        tag_to_id[tag_title] = tag.id
        tag_titles.append(tag_title)
    del tags, tag

    # Init argument parser.
    parser: ArgumentParser = ArgumentParser()

    # Add arguments.
    parser.add_argument(
        "--limit", type=int, help="Limit.", default=10, choices=range(1, 101)
    )
    parser.add_argument("--offset", type=int, help="Offset.", default=0)
    parser.add_argument(
        "-i",
        "--include-tag",
        type=str,
        action="append",
        choices=tag_titles,
        help="Tag to include.",
        default=[],
    )
    parser.add_argument(
        "--includedTagsMode",
        type=str,
        choices=["AND", "OR"],
        help="Included tags mode.",
        default="AND",
    )
    parser.add_argument(
        "-e",
        "--exclude-tag",
        type=str,
        action="append",
        choices=tag_titles,
        help="Tag to exclude.",
        default=[],
    )
    del tag_titles
    parser.add_argument(
        "--excludedTagsMode",
        type=str,
        choices=["AND", "OR"],
        help="Excluded tags mode.",
        default="OR",
    )
    parser.add_argument(
        "-s",
        "--status",
        type=str,
        action="append",
        choices=["ongoing", "completed", "hiatus", "cancelled"],
        help="Status.",
        default=[],
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Title.",
        default=None,
    )
    parser.add_argument(
        "-ol",
        "--original-language",
        type=str,
        action="append",
        choices=[
            "ja",
            "ko",
            "zh",
            "zh-hk",
            "en",
            "ar",
            "bn",
            "bg",
            "my",
            "ca",
            "hr",
            "cs",
            "da",
            "nl",
            "et",
            "tl",
            "fi",
            "fr",
            "de",
            "el",
            "he",
            "hi",
            "hu",
            "id",
            "it",
            "lt",
            "ms",
            "mn",
            "ne",
            "no",
            "fa",
            "pl",
            "pt",
            "pt-br",
            "ro",
            "ru",
            "sr",
            "es",
            "es-la",
            "sv",
            "th",
            "tr",
            "uk",
            "vi",
        ],
        help="Original language.",
        default=[],
    )
    parser.add_argument(
        "-pd",
        "--publication-demographic",
        type=str,
        action="append",
        choices=["shounen", "shoujo", "josei", "seinen", "none"],
        help="Publication demographic.",
        default=[],
    )
    parser.add_argument(
        "-id",
        type=str,
        action="append",
        help="Id.",
        default=[],
    )
    parser.add_argument(
        "-cr",
        "--content-rating",
        type=str,
        action="append",
        choices=["safe", "suggestive", "erotica", "pornographic"],
        help="Content rating.",
        default=[],
    )
    parser.add_argument(
        "--created-at-since", type=TypeDate(), help="Created at since.", default=None
    )
    parser.add_argument(
        "--updated-at-since", type=TypeDate(), help="Updated at since.", default=None
    )
    parser.add_argument("--year", type=int, help="Year of release.", default=None)
    parser.add_argument(
        "--mal-mangalist-file",
        type=FileType("r"),
        help="MAL mangalist from https://myanimelist.net/panel.php?go=export",
        default=None,
    )
    parser.add_argument(
        "--mal-download",
        action=BooleanOptionalAction,
        help="Download MAL mangalist from https://myanimelist.net/panel.php?go=export and save it to database.",
        default=False,
    )
    parser.add_argument(
        "--mangadex-force-load",
        action=BooleanOptionalAction,
        help="Force loading MangaDex data from API?",
        default=False,
    )

    def dir_path(string: str) -> str:
        """Check if given string argument is directory path.

        Args:
            string (str): Argument to check.

        Raises:
            NotADirectoryError: If was not directory path.

        Returns:
            str: Given argument.
        """

        if isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    parser.add_argument(
        "--data-directory",
        dest="data_directory",
        type=dir_path,
        default=working_directory,
        help="Data directory",
    )

    # Parse argumenst.
    args: Namespace = parser.parse_args()
    del parser

    # Init parameters for MangaDex call.
    pars: Dict = {}

    # Missing parameters:
    # authors : `List[str]` Array of strings <uuid>
    # artist : `List[str]` Array of strings <uuid>

    # Set parameters from arguments.
    pars["limit"] = args.limit
    pars["offset"] = args.offset
    pars["title"] = args.title
    pars["year"] = args.year

    # Add included tags.
    tags: List = args.include_tag
    if tags:
        pars["includedTags"] = []
        tag: str
        for tag in tags:
            pars["includedTags"].append(tag_to_id[tag])
        del tag
        pars["includedTagsMode"] = args.includedTagsMode
    del tags

    # Add excluded tags.
    tags: List = args.exclude_tag
    if tags:
        pars["excludedTags"] = []
        tag: str
        for tag in tags:
            pars["excludedTags"].append(tag_to_id[tag])
        del tag
        pars["excludedTagsMode"] = args.excludedTagsMode
    del tags
    del tag_to_id

    pars["status"] = args.status
    pars["originalLanguage"] = args.original_language
    pars["publicationDemographic"] = args.publication_demographic
    pars["ids"] = args.id
    pars["contentRating"] = args.content_rating

    # Add datetime pars.
    datetime_format: str = "%Y-%m-%dT%H:%M:%S"
    if args.created_at_since:
        pars["createdAtSince"] = args.created_at_since.strftime(datetime_format)
    if args.updated_at_since:
        pars["updatedAtSince"] = args.updated_at_since.strftime(datetime_format)
    del datetime_format

    # Data directory.
    data_directory: str = Dir(args.data_directory)
    # Connect to database.
    db: Database = Database(database_path=data_directory.file_path("database.db"))
    # Generate MAL manga list.
    mal: dict[int, MALManga] = MALManga.generate_list(
        db=db,
        data_directory=data_directory,
        file=args.mal_mangalist_file,
        download=args.mal_download,
    )
    # Get statuses.
    manga_dex: dict[str, MangaDexManga] = api.status(
        db=db, force_load=args.mangadex_force_load
    )
    # Disconnect from database.
    db.disconnect()
    del db

    del args

    # Remove None and [] values from parameters.
    pars = {
        k: v for k, v in pars.items() if v is not None and (v or type(v) is not list)
    }

    # Status to skip.
    manga_dex_status_to_skip: set = {
        MangaDexStatus.READING,
        MangaDexStatus.DROPPED,
        MangaDexStatus.RE_READING,
        MangaDexStatus.COMPLETED,
    }
    mal_status_to_skip: set = {
        MALStatus.COMPLETED,
        MALStatus.DROPPED,
    }

    # Init data.
    data: dict[str, list[dict[str, Union[str, int]]]] = {
        "licenced": [],
        "non_licenced": [],
    }

    def mangaupdates(id: int) -> Union[dict, None]:
        """Get MangaUpdates data.

        Args:
            id (int): MangaUpdates id.

        Returns:
            Union[dict, None]: Data or None if failed to get.
        """
        try:
            return series(id)
        except AttributeError as e:
            print(e)
            return None

    # Loop manga.
    for manga in api.get_manga_list(**pars):
        # Get title.
        title: str = "???"
        if "en" in manga.title:
            title = manga.title["en"]
        elif "jp" in manga.title:
            title = manga.title["jp"]
        elif manga.title:
            title = list(manga.title.values())[0]

        # Get own status.
        mangadex_manga: MangaDexManga = (
            manga_dex[manga.manga_id]
            if manga.manga_id in manga_dex
            else MangaDexManga(id=manga.manga_id, status=MangaDexStatus.NONE)
        )

        # Print manga and status.
        print(
            "{title}: {status}".format(title=title, status=mangadex_manga.status.name)
        )

        # Skip if status is one to skip.
        if mangadex_manga.status in manga_dex_status_to_skip:
            continue

        # Get links.
        links: Dict[str, str] = manga.links or []
        mal_manga: Union[MALManga, None] = None
        # If MyAnimelist link found.
        if "mal" in links:
            # Get MyAnimeList id.
            mal_id = int(links["mal"])

            # Get MALManga object.
            if mal_id in mal:
                mal_manga = mal[mal_id]
                if mal_manga.status in mal_status_to_skip:
                    print(
                        "\tFound with MAL status {status} so skipping!".format(
                            status=mal_manga.status.name
                        )
                    )
                    continue
            else:
                mal_manga = MALManga(
                    id=mal_id, volumes=0, chapters=0, status=MALStatus.NONE
                )
                mal[mal_id] = mal_manga
            del mal_id
        else:
            print("\tManga not in MAL so skipping!")
            continue

        # Init as not licenced.
        licenced = False

        # If has mangaupdates.com link.
        if "mu" in links:
            # Get mangaupdates.com id.
            mangaupdates_id = int(links["mu"])

            # Get mangaupdates.com data.
            manga_updates_manga: Union[dict, None] = store(
                data_directory=data_directory,
                key="manga_updates_{id}".format(id=mangaupdates_id),
                value=lambda: mangaupdates(mangaupdates_id),
            )
            del mangaupdates_id
            if manga_updates_manga is None:
                print("\tCould not get mangaupdates data!")
                continue

            # Get english publisher.
            if manga_updates_manga["licensed"]:
                if manga_updates_manga["english_publisher"]["name"]:
                    english_publisher: str = manga_updates_manga["english_publisher"][
                        "name"
                    ]
                else:
                    english_publisher: str = "?"
                licenced = True
                print(
                    "\tPublished in english by {publisher} so skipping!".format(
                        publisher=english_publisher
                    )
                )
        del links

        # Check that 5 or more new chapters are found.
        chapters: list[Chapter] = api.manga_feed(
            mangadex_manga.id,
            **{"translatedLanguage": ["en"], "order[chapter]": "desc", "limit": 1}
        )
        chapters: int = (
            floor(chapters[0].chapter)
            if chapters and chapters[0] and chapters[0].chapter
            else 0
        )
        if chapters < (mal_manga.chapters + 5):
            print("\tNo 5 or more new chapters found!")
            continue
        del chapters

        # Add data.
        data["licenced" if licenced else "non_licenced"].append(
            {
                "id": mangadex_manga.id,
                "title": title,
                "volumes": mal_manga.volumes,
                "chapters": mal_manga.chapters,
            }
        )
        del licenced
        print("\tADDED!")

    del api, pars, manga_dex_status_to_skip, mal_status_to_skip

    # Get public directory.
    public_dir = Dir("output", data_directory)
    del data_directory

    # Write data to JSON-files
    unique: str = "".join(choices(population=ascii_lowercase, k=10))
    timestr = strftime("%Y%m%d_%H%M%S")
    for key, mangas in data.items():
        # Skip if empty.
        if not mangas:
            print("{key}: EMPTY".format(key=key))
            continue
        # Short from most read chapters to least.
        mangas.sort(key=lambda manga: manga.get("chapters"), reverse=True)
        # Generate filepath.
        file_path: str = public_dir.file_path(
            "{timestr}_{unique}_{key}.json".format(
                key=key, timestr=timestr, unique=unique
            )
        )
        # Write data to JSON-file.
        with open(file_path, "w") as file:
            json.dump(mangas, file)
            file.close()
            print("{key}: {file_path}".format(key=key, file_path=file_path))
            del file
        del key, mangas, file_path
    del data, unique, timestr

    # Exit with success.
    exit(0)
