from pymongo import MongoClient


class MongoDBConnector:
    def __init__(self, db_name: str, username: str, password: str, cluster_uri: str) -> None:
        self.client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster_uri}/{db_name}')
        self.db = self.client[db_name]