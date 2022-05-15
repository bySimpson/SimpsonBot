import discord
import requests
from discord.ext import commands


class Duck(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="duck", description="Send a random duck in chat! (https://random-d.uk/)")
    async def clear(self, ctx: discord.commands.context.ApplicationContext):
        req = requests.get("https://random-d.uk/api/random")
        if req.status_code == 200:
            await ctx.respond(f"{req.json()['url']}")
        else:
            await ctx.respond(f"Not able to use https://random-d.uk API!", delete_after=5)


def setup(bot):
    bot.add_cog(Duck(bot))