from discord.ext import commands
from src.helper import *


class Help(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="help", description="Get list of all commands with description!")
    async def clear(self, ctx: discord.commands.context.ApplicationContext):
        description_dict = {}
        all_commands = self.bot.all_commands
        for id_ in all_commands:
            description_dict[all_commands[id_].name] = all_commands[id_].description
        description_dict = dict(sorted(description_dict.items()))
        embed_ = discord.Embed(title="Commands", color=0xb87328)
        for c_command in description_dict:
            embed_.add_field(name=f"/{c_command}", value=description_dict[c_command], inline=False)
        await ctx.respond(embed=embed_)


def setup(bot):
    bot.add_cog(Help(bot))