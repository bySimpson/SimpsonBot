from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class Guild(MongoModel):
    guild_id = fields.IntegerField(primary_key=True)
    users = fields.EmbeddedDocumentListField("User")


class User(MongoModel):
    user_id = fields.IntegerField(primary_key=True)
    moderator = fields.BooleanField(default=False)
    administrator = fields.BooleanField(default=False)