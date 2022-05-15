import discord
import os # default module
from decouple import config

extensions = [
    "clear",
    "duck",
    "mention",
    "help",
    "permissions"
]

def start_bot():

    bot = discord.Bot(debug_guilds=[170834267721564160], intents=discord.Intents.all(),
                      activity=discord.Activity(type=discord.ActivityType.playing, name="/help - by LordSimpson"))

    for cog in extensions:
        bot.load_extension(f"src.cogs.{cog}")

    bot.run(config('TOKEN')) # run the bot with the token