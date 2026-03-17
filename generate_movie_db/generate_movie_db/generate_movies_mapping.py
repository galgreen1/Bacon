import sqlite3
from gzip import decompress
from urllib.request import urlopen
from generate_movie_db.constants import SAVE_TITLES_FILE, MOVIE_TITLE, MOVIE_ID, MOVIES_TABLE


MOVIES_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"
IDENTIFIER_INDEX = 0
MOVIE_TITLE_INDEX = 3


def read_imdb_movies_names() -> None:
    """
    Read from the url all the infomation about movies titles
    Saves in a text file all of the movies information
    """
    with urlopen(MOVIES_URL) as f:
        with open(
            SAVE_TITLES_FILE,
            "w",
        ) as tmp_file:
            tmp_file.write(decompress(f.read()).decode())


def create_movies_to_identifier_mapping(db_name: str):
    """
    Create a table in the db that maps between movie name to its uid
    Save in each row the uid of the movie and the movie title.
    Read all of the movies information from a text file.
    """
    read_imdb_movies_names()
    con = sqlite3.connect(db_name)
    #  For forgien keys
    con.execute('PRAGMA foreign_keys = ON;')
    cur = con.cursor()
    cur.execute(f"CREATE TABLE {MOVIES_TABLE}({MOVIE_TITLE} TEXT, {MOVIE_ID} TEXT PRIMARY KEY)")
    with open(SAVE_TITLES_FILE) as titles_file:
        _ = titles_file.readline()  # titles
        lines = titles_file.read().split("\n")
        for line in lines:
            if line:
                splitted_line = line.split("\t")
                name = splitted_line[MOVIE_TITLE_INDEX]
                id = splitted_line[IDENTIFIER_INDEX]
                cur.execute(
                    f"INSERT INTO movie ({MOVIE_TITLE}, {MOVIE_ID}) VALUES (?, ?)",
                    (name, id),
                )
        con.commit()
    con.close()