import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="clear", description="Clear a set amount of messages")
    async def clear(self, ctx: discord.commands.context.ApplicationContext,
                    amount: discord.Option(discord.SlashCommandOptionType.integer, "amount", required=True),
                    user: discord.Option(discord.SlashCommandOptionType.user, "username", required=False)):
        if ctx.author.guild_permissions.administrator:
            if user:
                await ctx.channel.purge(limit=amount, check=lambda m: m.author.id == user.id)
                await ctx.respond(f"Cleared last {amount} messages of {user}!", delete_after=5)
            else:
                await ctx.channel.purge(limit=amount)
                await ctx.respond(f"Cleared last {amount} messages!", delete_after=5)
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)


def setup(bot):
    bot.add_cog(Clear(bot))