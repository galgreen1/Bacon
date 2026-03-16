from generate_movie_db.constants import (
    PLAYER_TO_MOVIE_TABLE,
    DB_NAME,
    ACTOR_ID,
    ACTOR_MOVIES,
    ACTOR_NAME,
)
from sqlite3 import connect
from typing import Union, List
from collections import deque
from math import inf
from time import time


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
    cur.execute(
        f"SELECT {ACTOR_ID}, {ACTOR_NAME}, {ACTOR_MOVIES} FROM {PLAYER_TO_MOVIE_TABLE} WHERE {ACTOR_NAME} = '{actor_name}'"
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
        f"SELECT {ACTOR_ID}, {ACTOR_NAME}, {ACTOR_MOVIES} FROM {PLAYER_TO_MOVIE_TABLE} WHERE {ACTOR_ID} = '{actor_uid}'"
    )
    row = cur.fetchone()
    con.close()
    if not row:
        raise Exception(f"actor {actor_uid} not found in the db")
    return (row[ACTOR_MOVIES_INDEX]).split(",")


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
    conditions = " OR ".join([f"(',' || {ACTOR_MOVIES} || ',') LIKE ?" for _ in movies])
    query = f"SELECT * FROM {PLAYER_TO_MOVIE_TABLE} WHERE {conditions}"
    params = [f"%,{movie},%" for movie in movies]
    cur.execute(query, params)
    rows = cur.fetchall()
    neighbors = []
    for row in rows:
        neighbors.append(row[ACTOR_ID_INDEX])
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
    current_Time = time()
    if dst_actor == source_actor:
        return 0
    uid_time = time()
    source_actor_id = get_actor_uid(source_actor)
    dst_actor_id = get_actor_uid(dst_actor)
    uid_finish_time = time()
    print('uid time:', uid_finish_time - uid_time)
    visited = []
    queue = deque([])
    queue.append((source_actor_id, 0))
    while queue:
        (actor, distance) = queue.popleft()
        college_time = time()
        colleagues = get_colleagues(actor)
        print('colleagues time', time() - college_time)
        for actor_colleague in colleagues:
            loop_time = time()
            if actor_colleague == dst_actor_id:
                finish_time = time()
                print('time:', finish_time - current_Time)
                return distance + 1
            if actor_colleague not in visited:
                visited.append(actor_colleague)
                queue.append((actor_colleague, distance + 1))
                #print('loop time:', time() - loop_time)
    finish_time = time()
    print('time:', finish_time - current_Time)
    return inf


if __name__ == "__main__":
    print(compute_distance('Kevin Bacon', 'Paul Brickman'))
    