import pymongo

CONNECTION = "mongodb://localhost:27017/"
MONGO_NAME = "colleagues"
COLLECTION_NAME = "actors_collegues"


def create_mongo_db() -> None:
    client = pymongo.MongoClient(CONNECTION)

    # 2. Access a database (e.g., 'user_shopping_list')
    # MongoDB doesn't create the database until data is inserted
    dbname = client[MONGO_NAME]

    # 3. Access a collection (e.g., 'item_details')
    collection_name = dbname[COLLECTION_NAME]


