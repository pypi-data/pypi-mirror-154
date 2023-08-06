from pymongo import MongoClient
from pymongo import database as mongo_database
from os import environ


class MongoWrapper:
    _client: MongoClient
    db: mongo_database

    def __init__(self, host: str = None, port: int = None, user: str = None, password: str = None,
                 database: str = None) -> None:
        self.host = host or environ.get('MONGODB_HOST')
        self.port = port or int(environ.get('MONGODB_PORT'))
        self.user = user or environ.get('MONGODB_USER')
        self.password = password or environ.get('MONGODB_PASSWORD')
        self.database = database or environ.get('MONGODB_DB')
        self._connect()

    def _connect(self) -> None:
        self._client = MongoClient(
            host=self.host, port=self.port, username=self.user, password=self.password
        )
        self.db = self._client[self.database]

    def get(self, table: str, query: dict = None):
        return self.db[table].find(query)

    def get_one(self, table: str, query: dict) -> dict:
        return self.db[table].find_one(filter=query)

    def put(self, table: str, data: dict):
        self.db[table].insert_one(data)

    def update(self, table: str, update_data: dict, id_dict: dict):
        self.db[table].update_one(
            id_dict,
            {'$set': update_data}
        )

    def upsert(self, table: str, data: dict, id_dict: dict):
        self.db[table].update_one(id_dict, {'$set': data}, upsert=True)

    def delete_one(self, table: str, id_dict: dict) -> None:
        self.db[table].delete_one(id_dict)

    def delete_many(self, table: str, id_dict: dict) -> None:
        self.db[table].delete_many(id_dict)


def setup_db(mongo: MongoWrapper) -> None:
    collects = ['dex_pools', 'tokens', 'dex_configs']
    dex_pools = mongo.db['dex_pools']
    dex_pools.create_index([('address', 1), ('dex', 1)], unique=True)
