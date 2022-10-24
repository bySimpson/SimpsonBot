import discord
from discord.ext import commands
import time


class Mention(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Ping a user!")
    async def clear(self, ctx: discord.commands.context.ApplicationContext,
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True),
                    amount: discord.Option(discord.SlashCommandOptionType.integer, "amount", required=False)):
        if amount:
            await ctx.respond(f"Pinging {username} {amount} times!", delete_after=3)
            for i in range(0, amount):
                await ctx.send(f"<@{username.id}>")
                time.sleep(2)
        else:
            await ctx.respond(f"Pinging {username}!", delete_after=3)
            await ctx.send(f"<@{username.id}>")


def setup(bot):
    bot.add_cog(Mention(bot))