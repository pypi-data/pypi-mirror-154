# MyAnimelist Manga and Anime -list downloader

Download manga or anime list from MyAnimeList.

## Install
Install [myanimelist_downloader](https://pypi.org/project/myanimelist-downloader/)-package from The Python Package Index (PyPI).
```shell
pip install myanimelist_downloader
```

## Usage
```shell
usage: myanimelist_downloader [-h] [-u USERNAME] [-p PASSWORD] [-d DOWNLOAD_DIRECTORY] [-e ENV_FILE] [-a | --anime | --no-anime] [-m | --manga | --no-manga]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        MyAnimeList username
  -p PASSWORD, --password PASSWORD
                        MyAnimeList password
  -d DOWNLOAD_DIRECTORY, --download-directory DOWNLOAD_DIRECTORY
                        Download directory
  -e ENV_FILE, --env-file ENV_FILE
                        Enviroment file
  -a, --anime, --no-anime
                        Download mangalist. (default: False)
  -m, --manga, --no-manga
                        Download mangalist. (default: False)
```