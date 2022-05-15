from typing import Any

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connection
import json
from src.models import *
from decouple import config


class Config:
    def __init__(self, path="./src/config/config.json"):
        self._path = path
        with open(self._path) as file:
            self._data = json.load(file)
            self._file = file

    def reload_file(self):
        with open(self._path) as file:
            self._data = json.load(file)
            self._file = file

    def read_config_file(self, key):
        self.reload_file()
        try:
            return self._data[key]
        except Exception:
            return None

    def set_config_file(self, key, value):
        self.reload_file()
        self._data[key] = value
        with open(self._path, "w") as write_file:
            json.dump(self._data, write_file, ensure_ascii=False, indent=4)
        self.reload_file()

    def get_whole_file(self):
        self.reload_file()
        return self._data


class DB:
    def __init__(self):
        self.__username = config("MONGODB_USERNAME", cast=str)
        self.__password = config("MONGODB_PASSWORD", cast=str)
        self.__hostname = config("MONGODB_URL", default="localhost", cast=str)
        self.__document = config("MONGODB_DOCUMENT", default="orderservice", cast=str)
        self.__connection_string = f"mongodb://{self.__username}:{self.__password}@{self.__hostname}/SimpsonBot?authSource=admin"

        connection.connect(self.__connection_string)

    def insert_guild(self, guild_id: int):
        c_guild = Guild(guild_id=guild_id)
        c_guild.save()
        return c_guild

    def get_guild_by_id(self, guild_id: int) -> Guild | None:
        try:
            return Guild.objects.get({"_id": guild_id})
        except Exception:
            return None

    def update_or_add_user_to_guild(self, guild_id: int, user_id: int, user_object: User):
        user_object.user_id = user_id
        guild = self.get_guild_by_id(guild_id)
        if not guild:
            guild = self.insert_guild(guild_id)

        found = False
        for i in range(0, len(guild.users)):
            if guild.users[i].user_id == user_id:
                guild.users[i] = user_object
                found = True
                break
        if not found:
            guild.users.append(user_object)
        guild.save()
        return user_object

    def get_user(self, guild_id: int, user_id: int) -> User | None:
        try:
            guild = Guild.objects.get({"_id": guild_id, "users._id": user_id})
            for user in guild.users:
                if user.user_id == user_id:
                    return user
        except Exception:
            return None

    def is_admin(self, guild_id, user_id):
        user = self.get_user(guild_id, user_id)
        if user:
            return user.administrator
        else:
            return False

    def is_moderator(self, guild_id, user_id):
        user = self.get_user(guild_id, user_id)
        if user:
            if user.administrator or user.moderator:
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    db = DB()
    #db.insert_guild(170834267721564160)
    #db.get_guild_by_id(170834267721564160)
    #db.set_permissions_of_user(170834267721564160, 1)
    db.update_or_add_user_to_guild(170834267721564160, 416678961079386142, User(administrator=True))
    print(db.is_moderator(170834267721564160, 416678961079386142))