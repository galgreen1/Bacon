from generate_movie_db.constants import (
    ACTOR_TABLE,
    DB_NAME,
    ACTOR_ID,
    ACTOR_MOVIES,
    ACTOR_NAME,
)
from sqlite3 import connect
from typing import Union, List
from heapdict import heapdict
from math import inf


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
    return (row[ACTOR_MOVIES_INDEX]).split(",")


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


def instalize_min_heap() -> heapdict:
    """
    Instalize a min heap with a distance equal infinity for each actor
    and the actor uid
    Puts each actor inside the queue
    """
    min_heap = heapdict()
    con = connect(DB_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {ACTOR_TABLE}")
    while True:
        #  Fetch in batches
        rows = cur.fetchmany(size=BATCH_SIZE)
        if not rows:
            break
        for row in rows:
            #  Instalize all distances to infinity
            min_heap[row[ACTOR_ID_INDEX]] = inf
    return min_heap


def check_if_colleagues(first_actor_uid: str, second_actor_uid: str) -> bool:
    """
    Returns if the given actors have worked in the same movie

    :first_actor_uid: The uid of one actor
    :second_actor_uid: The uid of the second actor
    """
    first_actor_movies = get_actor_movies(first_actor_uid)
    second_actor_movies = get_actor_movies(second_actor_uid)
    if first_actor_movies == "/N" or second_actor_movies == "/N":
        #  If there isnt any data on movies one of the players worked in
        return False
    for movie in first_actor_movies:
        if movie in second_actor_movies:
            return True
    return False


def compute_distance(source_actor: str, dst_actor: str) -> Union[int, float]:
    """
    Compute the distance between 2 actors
    returns an int if its a final number, otherwise infinity
    Dijkstra's algorithm implementition

    :source_actor_uid: The name of one actor
    :dst_actor_uid: The name of the second actor
    """
    min_heap = instalize_min_heap()
    #  Instalize the source distance from himself to 0
    min_heap[get_actor_uid(source_actor)] = 0
    while len(min_heap) > 0:
        current_actor_uid, distance = min_heap.popitem()
        #  If reached infinity distance there is no point in keep going
        if distance == inf:
            return inf
        #  If this is the distance we search we stop and return
        if current_actor_uid == get_actor_uid(dst_actor):
            return distance
        for actor in min_heap.keys():
            if check_if_colleagues(actor, current_actor_uid):
                if min_heap[actor] > distance + 1:
                    min_heap[actor] = distance + 1
    raise Exception(f"destinition actor {dst_actor} not in the db")
