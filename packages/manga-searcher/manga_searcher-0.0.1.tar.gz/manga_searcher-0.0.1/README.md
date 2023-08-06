# Manga searcher.

Search new manga to read.

## Install
Install [manga_searcher](https://pypi.org/project/manga-searcher/)-package from The Python Package Index (PyPI).
```shell
pip install manga_searcher
```

## Usage
```shell
usage: manga_searcher [-h]
                      [--limit {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100}]
                      [--offset OFFSET]
                      [-i {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}]
                      [--includedTagsMode {AND,OR}]
                      [-e {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}]
                      [--excludedTagsMode {AND,OR}] [-s {ongoing,completed,hiatus,cancelled}] [--title TITLE]
                      [-ol {ja,ko,zh,zh-hk,en,ar,bn,bg,my,ca,hr,cs,da,nl,et,tl,fi,fr,de,el,he,hi,hu,id,it,lt,ms,mn,ne,no,fa,pl,pt,pt-br,ro,ru,sr,es,es-la,sv,th,tr,uk,vi}]
                      [-pd {shounen,shoujo,josei,seinen,none}] [-id ID] [-cr {safe,suggestive,erotica,pornographic}] [--created-at-since CREATED_AT_SINCE] [--updated-at-since UPDATED_AT_SINCE] [--year YEAR]
                      [--mal-mangalist-file MAL_MANGALIST_FILE] [--mal-download | --no-mal-download] [--mangadex-force-load | --no-mangadex-force-load] [--data-directory DATA_DIRECTORY]

options:
  -h, --help            show this help message and exit
  --limit {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100}
                        Limit.
  --offset OFFSET       Offset.
  -i {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}, --include-tag {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}
                        Tag to include.
  --includedTagsMode {AND,OR}
                        Included tags mode.
  -e {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}, --exclude-tag {Oneshot,Thriller,Award Winning,Reincarnation,Sci-Fi,Time Travel,Genderswap,Loli,Traditional Games,Official Colored,Historical,Monsters,Action,Demons,Psychological,Ghosts,Animals,Long Strip,Romance,Ninja,Comedy,Mecha,Anthology,Boys' Love,Incest,Crime,Survival,Zombies,Reverse Harem,Sports,Superhero,Martial Arts,Fan Colored,Samurai,Magical Girls,Mafia,Adventure,User Created,Virtual Reality,Office Workers,Video Games,Post-Apocalyptic,Sexual Violence,Crossdressing,Magic,Girls' Love,Harem,Military,Wuxia,Isekai,4-Koma,Doujinshi,Philosophical,Gore,Drama,Medical,School Life,Horror,Fantasy,Villainess,Vampires,Delinquents,Monster Girls,Shota,Police,Web Comic,Slice of Life,Aliens,Cooking,Supernatural,Mystery,Adaptation,Music,Full Color,Tragedy,Gyaru}
                        Tag to exclude.
  --excludedTagsMode {AND,OR}
                        Excluded tags mode.
  -s {ongoing,completed,hiatus,cancelled}, --status {ongoing,completed,hiatus,cancelled}
                        Status.
  --title TITLE         Title.
  -ol {ja,ko,zh,zh-hk,en,ar,bn,bg,my,ca,hr,cs,da,nl,et,tl,fi,fr,de,el,he,hi,hu,id,it,lt,ms,mn,ne,no,fa,pl,pt,pt-br,ro,ru,sr,es,es-la,sv,th,tr,uk,vi}, --original-language {ja,ko,zh,zh-hk,en,ar,bn,bg,my,ca,hr,cs,da,nl,et,tl,fi,fr,de,el,he,hi,hu,id,it,lt,ms,mn,ne,no,fa,pl,pt,pt-br,ro,ru,sr,es,es-la,sv,th,tr,uk,vi}
                        Original language.
  -pd {shounen,shoujo,josei,seinen,none}, --publication-demographic {shounen,shoujo,josei,seinen,none}
                        Publication demographic.
  -id ID                Id.
  -cr {safe,suggestive,erotica,pornographic}, --content-rating {safe,suggestive,erotica,pornographic}
                        Content rating.
  --created-at-since CREATED_AT_SINCE
                        Created at since.
  --updated-at-since UPDATED_AT_SINCE
                        Updated at since.
  --year YEAR           Year of release.
  --mal-mangalist-file MAL_MANGALIST_FILE
                        MAL mangalist from https://myanimelist.net/panel.php?go=export
  --mal-download, --no-mal-download
                        Download MAL mangalist from https://myanimelist.net/panel.php?go=export and save it to database. (default: False)
  --mangadex-force-load, --no-mangadex-force-load
                        Force loading MangaDex data from API? (default: False)
  --data-directory DATA_DIRECTORY
                        Data directory
```

## Enviroment
| ENV                            | Description                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| MANGA_DEX_USERNAME             | MangaDex username.                                                                       |
| MANGA_DEX_PASSWORD             | MangaDex password.                                                                       |
| MAL_USERNAME                   | MyAnimeList username.                                                                    |
| MAL_PASSWORD                   | MyAnimeList password.                                                                    |
| SELENIUM_NO_SANDBOX            | Run Chrome without sandbox.                                                              |
| SELENIUM_DISABLE_DEV_SHM_USAGE | Disable Chrome shared memory space.                                                      |
| SELENIUM_DISABLE_EXTENSIONS    | Disable Chrome extensions.                                                               |
| SELENIUM_DISABLE_GPU           | Disable Graphics Processing Unit with Chrome.                                            |
| SELENIUM_DEBUG                 | Turn on/off Selenium debuging.When true, run Chrome with head and do not close on error. |

## Packages

### [argparse](https://github.com/ThomasWaldmann/argparse/)
Command line argument parser.

### [mangadex](https://github.com/EMACC99/mangadex)
Wrapper for MangaDex API.

### [py-manga](https://github.com/emily-signet/py-manga)
Library for getting information from mangaupdates.com!

### [typedate](https://github.com/righ/typedate)
Add date support for arguments.

### [myanimelist-downloader](https://github.com/SanteriHetekivi/myanimelist_downloader)
My other library for downloading MyAnimeList lists.