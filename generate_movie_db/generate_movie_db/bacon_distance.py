from generate_movie_db.constants import (
    ACTOR_TABLE,
    DB_NAME,
    ACTOR_ID,
    ACTOR_NAME,
    MOVIE_ID,
    ACTOR_MOVIE_TABLE,
)
from generate_movie_db.exceptions import ActorNotFound
from sqlite3 import connect
from typing import Union, List
from collections import deque
from math import inf


KEVIN_BACON_NAME = "Kevin Bacon"
ACTOR_ID_INDEX = 0
ACTOR_MOVIES_INDEX = 2
MOVIE_ID_INDEX = 1


def get_actor_uid(actor_name: str) -> str:
    """
    Returns the uid of actor with this name
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        f"SELECT {ACTOR_ID}, {ACTOR_NAME} FROM {ACTOR_TABLE} WHERE {ACTOR_NAME} = '{actor_name}'"
    )
    row = cur.fetchone()
    con.close()
    if not row:
        raise ActorNotFound(actor_name)
    return row[ACTOR_ID_INDEX]


def get_actor_movies(actor_uid: str) -> List[str]:
    """
    Returns the movies of the actor with this id
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        f"SELECT {MOVIE_ID} FROM {ACTOR_MOVIE_TABLE} WHERE {ACTOR_ID} = '{actor_uid}'"
    )
    rows = cur.fetchall()
    con.close()
    if not rows:
        raise ActorNotFound(actor_uid)
    movies = [row[0] for row in rows]
    return movies


def get_colleagues(actor_uid: str) -> List[str]:
    """
    returns all of the ids of actors that played in the same movies
    as the given actor
    """
    con = connect(DB_NAME)
    cur = con.cursor()
    movies = get_actor_movies(actor_uid)
    if len(movies) == 0:
        con.close()
        return []
    placeholders = ", ".join("?" * len(movies))
    cur.execute(
        f"SELECT DISTINCT {ACTOR_ID} FROM {ACTOR_MOVIE_TABLE} WHERE {MOVIE_ID} IN ({placeholders})",
        movies,
    )
    rows = cur.fetchall()
    neighbors = [row[0] for row in rows]
    con.close()
    return neighbors


def compute_distance(source_actor: str, dst_actor: str) -> Union[int, float]:
    """
    Compute the distance between 2 actors
    returns an int if its a final number, otherwise infinity
    BFS algorithm implementition

    :source_actor_uid: The name of one actor
    :dst_actor_uid: The name of the second actor
    """
    if dst_actor == source_actor:
        return 0
    source_actor_id = get_actor_uid(source_actor)
    dst_actor_id = get_actor_uid(dst_actor)
    visited = []
    queue: deque = deque([])
    queue.append((source_actor_id, 0))
    while queue:
        (actor, distance) = queue.popleft()
        colleagues = get_colleagues(actor)
        for actor_colleague in colleagues:
            if actor_colleague == dst_actor_id:
                return distance + 1
            if actor_colleague not in visited:
                visited.append(actor_colleague)
                queue.append((actor_colleague, distance + 1))
    return inf


def compute_bacon_distance(actor_name: str) -> Union[int, float]:
    """
    Compute the distance from kevin bacon
    """
    return compute_distance(KEVIN_BACON_NAME, actor_name)
