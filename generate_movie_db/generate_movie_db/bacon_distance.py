from generate_movie_db.constants import (
    ACTOR_TABLE,
    DB_NAME,
    ACTOR_ID,
    ACTOR_NAME,
    MOVIE_ID,
    ACTOR_MOVIE_TABLE
)
from sqlite3 import connect
from typing import Union, List
from collections import deque
from math import inf
from time import time


KEVIN_BACON_NAME = "Kevin Bacon"
ACTOR_ID_INDEX = 0
ACTOR_MOVIES_INDEX = 2
MOVIE_ID_INDEX = 1
BATCH_SIZE = 10000


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
        raise Exception(f"{actor_name} actor not found in the db")
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
        raise Exception(f"actor {actor_uid} not found in the db")
    movies = [row[0] for row in rows]
    return movies


def get_colleagues(actor_uid: str) -> List[str]:
    """
    returns all of the ids of actors that played in the same movies
    as the given actor
    """
    total=time()
    start=time()
    con = connect(DB_NAME)
    cur = con.cursor()
    movies = get_actor_movies(actor_uid)
    if len(movies) == 0:
        con.close()
        return []
    print('instalize', time()-start)
    placeholders = ', '.join('?' * len(movies))
    start=time()
    cur.execute(
        f"SELECT DISTINCT {ACTOR_ID} FROM {ACTOR_MOVIE_TABLE} WHERE {MOVIE_ID} IN ({placeholders})", movies
    )
    print('execute', time()-start)
    start=time()
    rows = cur.fetchall()
    print('fetch', time()-start)
    neighbors = [row[0] for row in rows]
    con.close()
    print('total', time()-total)
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
    queue = deque([])
    queue.append((source_actor_id, 0))
    start=time()
    while queue:
        (actor, distance) = queue.popleft()
        start_get=time()
        colleagues = get_colleagues(actor)
        print('get colleafues', time()-start_get)
        for actor_colleague in colleagues:
            if actor_colleague == dst_actor_id:
                print('time:', time()-start)
                return distance + 1
            if actor_colleague not in visited:
                visited.append(actor_colleague)
                queue.append((actor_colleague, distance + 1))
    return inf


if __name__ == "__main__":
    print(compute_distance(KEVIN_BACON_NAME, 'Robert Wagner'))
