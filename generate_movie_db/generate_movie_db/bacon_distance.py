from generate_movie_db.constants import ACTOR_TABLE, DB_NAME, ACTOR_ID, ACTOR_MOVIES, ACTOR_NAME
from sqlite3 import connect
from typing import Union, List, Tuple


KEVIN_BACON_NAME = "Kevin Bacon"
ACTOR_ID_INDEX = 0
ACTOR_MOVIES_INDEX = 2
BATCH_SIZE = 10000


def get_actor_uid(actor_name: str) -> str:
    """
    Returns the uid of actor with this name
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT {ACTOR_ID}, {ACTOR_NAME}, {ACTOR_MOVIES} FROM {ACTOR_TABLE} WHERE {ACTOR_NAME} = {actor_name}")
    row = cur.fetchone()
    con.close()
    if not row:
        raise Exception(f"{actor_name} actor not found in the db")
    return row[ACTOR_ID_INDEX]


def get_actor_movies(actor_uid: str) -> List[str]:
    """
    Returns the movies of the actor with this id
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT {ACTOR_ID}, {ACTOR_NAME}, {ACTOR_MOVIES} FROM {ACTOR_TABLE} WHERE {ACTOR_ID} = {actor_uid}")
    row = cur.fetchone()
    con.close()
    if not row:
        raise Exception(f"{actor_uid} actor not found in the db")
    return row[ACTOR_MOVIES_INDEX]


def get_actors_number() -> int:
    """
    Returns the number of actors in the db
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {ACTOR_TABLE}")
    row = cur.fetchone()
    con.close()
    if not row:
        raise Exception("non valid db- error in checking number of actors")
    return int(row[0])


def instalize_min_heap() -> List[Tuple[Union[int, float], str]]:
    """
    Instalize a min heap with a distance equal infinity for each actor
    and the actor uid
    Puts each actor inside the queue
    """
    heap = []
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {ACTOR_TABLE}")
    while True:
        rows = cur.fetchmany(size=BATCH_SIZE)
        if not rows:
            break
        for row in rows:




def compute_distance(source_actor: str, dst_actor: str) -> Union[int, float]:
    """
    Compute the distance between 2 actors
    returns an int if its a final number, otherwise infinity
    Dijkstra's algorithm implementition

    :source_actor_uid: The name of one actor
    :dst_actor_uid: The name of the second actor
    """

