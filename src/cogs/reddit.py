import discord
import requests
from discord.ext import commands


class Reddit(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    def get_meme_from_reddit(self, subreddit_name: str, show_title=True):
        response = requests.get(f"https://meme-api.herokuapp.com/gimme/{subreddit_name}")
        if response.status_code == 200:
            json_response = response.json()
            if "url" in json_response and "title" in json_response:
                if show_title:
                    return f"{json_response['title']}\n{json_response['url']}"
                else:
                    return json_response["url"]
        return None

    @discord.slash_command(name="programmerhumor", description="Get a random meme from ProgrammerHumor subreddit!")
    async def programmerhumor(self, ctx: discord.commands.context.ApplicationContext):
        meme = self.get_meme_from_reddit("ProgrammerHumor")
        if meme:
            await ctx.respond(meme)
        else:
            await ctx.respond(f"Not able to get meme from Reddit!", delete_after=5)

    @discord.slash_command(name="oddlysatisfying", description="Get a random meme from oddlysatisfying subreddit!")
    async def oddlysatisfying(self, ctx: discord.commands.context.ApplicationContext):
        meme = self.get_meme_from_reddit("oddlysatisfying")
        if meme:
            await ctx.respond(meme)
        else:
            await ctx.respond(f"Not able to get meme from Reddit!", delete_after=5)


def setup(bot):
    bot.add_cog(Reddit(bot))