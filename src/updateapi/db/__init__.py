from mongoengine import connect

from updateapi.config import config

mongo_uri = config.get("db.mongo_uri")
connect(mongo_uri)
