from sqlite3 import connect
from gzip import decompress
from urllib.request import urlopen
<<<<<<< HEAD
from generate_movie_db.constants import (
    SAVE_ACTORS_FILE,
    ACTOR_TABLE,
    ACTOR_ID,
    ACTOR_MOVIES,
    ACTOR_NAME,
    ACTOR_MOVIE_TABLE,
    MOVIE_ID,
    MOVIES_TABLE,
)
=======
from generate_movie_db.constants import SAVE_ACTORS_FILE, ACTOR_TABLE, ACTOR_ID, ACTOR_MOVIES, ACTOR_NAME
>>>>>>> 4634216 (wip)


ACTORS_URL = "https://datasets.imdbws.com/name.basics.tsv.gz"
ACTOR_ID_INDEX = 0
ACTOR_NAME_INDEX = 1
MOVIES_ID_INDEX = 5


def read_imdb_players_names() -> None:
    """
    Read from the url all the infomation about actors
    Saves in a text file all of the actors information
    """
    with urlopen(ACTORS_URL) as f:
        with open(
            SAVE_ACTORS_FILE,
            "w",
        ) as tmp_file:
            tmp_file.write(decompress(f.read()).decode())


def create_players_to_movies_mapping(db_name: str) -> None:
    """
    Create a table in the db that maps between actor to movies
    he participates at.
    Save in each row the uid of the actor, the actor name
    and the uids of movies he participates at.
    Read all of the actors information from a text file.
    """
    read_imdb_players_names()
    con = connect(db_name)
    #  For foreign keys
    con.execute('PRAGMA foreign_keys = ON;')
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE {ACTOR_TABLE}({ACTOR_ID} TEXT PRIMARY KEY, {ACTOR_NAME} TEXT)"
    )
    cur.execute(
        f"CREATE TABLE {ACTOR_MOVIE_TABLE}({ACTOR_ID} TEXT REFERENCES {ACTOR_TABLE}({ACTOR_ID}), {MOVIE_ID} TEXT)"
    )
    with open(SAVE_ACTORS_FILE) as actors_file:
        _ = actors_file.readline()  # titles
        lines = actors_file.read().split("\n")
        for line in lines:
            if line:
                splitted_line = line.split("\t")
                actor_id = splitted_line[ACTOR_ID_INDEX]
                actor_name = splitted_line[ACTOR_NAME_INDEX]
                movies_id = splitted_line[MOVIES_ID_INDEX]
                cur.execute(
                    f"INSERT INTO {ACTOR_TABLE} ({ACTOR_ID}, {ACTOR_NAME}) VALUES (?, ?)",
                    (actor_id, actor_name),
                )
        con.commit()
        for line in lines:
            if line:
                splitted_line = line.split("\t")
                actor_id = splitted_line[ACTOR_ID_INDEX]
                movies_id = splitted_line[MOVIES_ID_INDEX]
                if movies_id.strip() != '\\N':
                    for movie_uid in movies_id.split(','):
                        cur.execute(
                            f"INSERT INTO {ACTOR_MOVIE_TABLE} ({ACTOR_ID}, {MOVIE_ID}) VALUES (?, ?)",
                            (actor_id, movie_uid),
                        )
        con.commit()
    con.close()
