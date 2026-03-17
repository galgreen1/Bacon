from generate_movie_db.generate_movies_mapping import (
    create_movies_to_identifier_mapping,
)
from generate_movie_db.generate_players_to_movies_mapping import (
    create_players_to_movies_mapping,
)
from os import remove
from generate_movie_db.constants import SAVE_TITLES_FILE, SAVE_ACTORS_FILE, DB_NAME


def main() -> None:
    """
    Saving an sql db
    A mapping between actors to movies they participates at
    """
    create_movies_to_identifier_mapping(DB_NAME)
    create_players_to_movies_mapping(DB_NAME)
    #  Delete tmp files
    #  Assume the program get runned from inside its directory
    remove(SAVE_ACTORS_FILE)
    remove(SAVE_TITLES_FILE)


if __name__ == "__main__":
    main()
