import discord
import os  # default module
from decouple import config
from src.db import DB

extensions = [
    "clear",
    "duck",
    "help",
    "logging",
    "mention",
    "permissions",
    "randomGenerator",
    "reddit",
    "status",
    "version"
]

db = DB()

bot = discord.Bot(intents=discord.Intents.all(),
                  activity=discord.Activity(type=discord.ActivityType.playing, name="/help - by LordSimpson"))


def start_bot():
    for cog in extensions:
        bot.load_extension(f"src.cogs.{cog}")

    bot.run(config('TOKEN'))  # run the bot with the token
