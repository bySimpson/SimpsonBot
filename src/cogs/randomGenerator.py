from discord.ext import commands
from src.helper import *
from decouple import config
import random


class RandomGenerator(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="coinflip", description="Flip a coin!")
    async def coinflip(self, ctx: discord.commands.context.ApplicationContext):
        number = random.randint(0, 1)
        if number == 1:
            output = "Head"
        else:
            output = "Tail"
        await ctx.respond(f"{output}")

    @discord.slash_command(name="random", description="Random number between x and y!")
    async def random_number(self, ctx: discord.commands.context.ApplicationContext,
                   from_: discord.Option(discord.SlashCommandOptionType.integer, "from", required=True),
                   to_: discord.Option(discord.SlashCommandOptionType.integer, "to", required=True)):
        if from_ > to_:
            await ctx.respond(f"Your from number should be lower than your to number!", ephemeral=True)
        number = random.randint(from_, to_)
        await ctx.respond(f"Your number: {number}")


def setup(bot):
    bot.add_cog(RandomGenerator(bot))
