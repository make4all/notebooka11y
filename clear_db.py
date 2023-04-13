from pymongo import MongoClient

client = MongoClient()
client.drop_database("pa11y-webservice")

