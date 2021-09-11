from pymongo import MongoClient
from pprint import pprint
from parsingInstagram import settings

client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)

# Task 04
query_1 = {'from_username': 'machine_learning_with_python'}

# Task 05
query_2 = {'$and': [{'from_username': 'python.learning'},
                        {'user_status': 'following'}]}

data_1 = client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION].find(filter=query_1)
data_2 = client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION].find(filter=query_2)

for item in data_1:
    pprint(item)

for item in data_2:
    pprint(item)