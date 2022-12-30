import discord
from discord.ext import commands
from src.helper import *
from decouple import config
from src.helper import setup_logger


class Logging(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.logger = setup_logger()

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx: discord.commands.context.ApplicationContext):
        self.logger.info(get_log_text(guild=ctx.guild.name, user=ctx.user.display_name, message=f"used command {ctx.command.name}"))


def setup(bot):
    bot.add_cog(Logging(bot))
