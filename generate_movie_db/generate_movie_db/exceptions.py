from generate_movie_db.constants import ACTOR_NOT_FOUND_TEXT


class ActorNotFound(Exception):
    def __init__(self, actor_name: str) -> None:
        self.actor_name = actor_name
        super().__init__(ACTOR_NOT_FOUND_TEXT)
    
    def __str__(self):
        return self.actor_name + ACTOR_NOT_FOUND_TEXT
