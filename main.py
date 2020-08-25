from src.db import Config
from src.bot import Bot

if __name__ == "__main__":
    config = Config()
    botKey = config.read_config_file("bot_key")
    prefix = config.read_config_file("bot_prefix")
    if botKey != "":
        bot = Bot(botKey, prefix=prefix)
