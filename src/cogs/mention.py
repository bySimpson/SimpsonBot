import discord
from discord.ext import commands
import time
from discord import guild_only


class Mention(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @guild_only()
    @discord.slash_command(name="ping", description="Ping a user!")
    async def ping(self, ctx: discord.commands.context.ApplicationContext,
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
