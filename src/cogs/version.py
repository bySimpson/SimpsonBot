import discord
from discord.ext import commands
from src.helper import *
from decouple import config


class Version(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="version", description="Get current version of the bot!")
    async def help(self, ctx: discord.commands.context.ApplicationContext):
        version = config("VERSION", default="dev")
        if version == "%VER%":
            version = "0.0.0-dev"
        await ctx.respond(f"Current version: {version}")


def setup(bot):
    bot.add_cog(Version(bot))
