import discord
import requests
from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.update_service_status.start()

    @tasks.loop(minutes=5)
    async def update_service_status(self):
        requests.get("https://betteruptime.com/api/v1/heartbeat/MVLGr758LctjAWH1NqxijH6b")


def setup(bot):
    bot.add_cog(Status(bot))