import sqlite3
from gzip import decompress
from urllib.request import urlopen
from generate_movie_db.constants import SAVE_ACTORS_FILE


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
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("CREATE TABLE actors(actor_id, actor_name, movies_id)")
    with open(SAVE_ACTORS_FILE) as actors_file:
        _ = actors_file.readline()  # titles
        lines = actors_file.read().split("\n")
        for line in lines:
            splitted_line = line.split("\t")
            actor_id = splitted_line[ACTOR_ID_INDEX]
            actor_name = splitted_line[ACTOR_NAME_INDEX]
            movies_id = splitted_line[MOVIES_ID_INDEX]
            cur.execute(
                "INSERT INTO actors (actor_id, actor_name, movies_id) VALUES (?, ?, ?)",
                (actor_id, actor_name, movies_id),
            )
            con.commit()
    con.close()
