import discord
from discord.ext import commands
from src.models import User, Guild
from src.db import DB


class Clear(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.db = DB()
        self.bot = bot

    @discord.slash_command(name="clear", description="Clear a set amount of messages")
    async def clear(self, ctx: discord.commands.context.ApplicationContext,
                    amount: discord.Option(discord.SlashCommandOptionType.integer, "amount", required=True),
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=False)):
        if ctx.author.guild_permissions.administrator or self.db.is_moderator(ctx.guild_id, ctx.author.id):
            if username:
                await ctx.channel.purge(limit=amount, check=lambda m: m.author.id == username.id)
                await ctx.respond(f"Cleared last {amount} messages of {username}!", delete_after=5)
            else:
                await ctx.channel.purge(limit=amount)
                await ctx.respond(f"Cleared last {amount} messages!", delete_after=5)
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)


def setup(bot):
    bot.add_cog(Clear(bot))