import discord
from discord.ext import commands
from src.helper import *
from decouple import config
import time


class UserInfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="info", description="Get information about a specific user!")
    async def user_info(self, ctx: discord.commands.context.ApplicationContext,
                        username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True)):
        embed_ = discord.Embed(title=f"Information about: {username}", color=0xb87328, description="Desc")
        embed_.set_thumbnail(url=username.display_avatar.url)
        embed_.add_field(name=f"ID", value=username.id, inline=True)
        embed_.add_field(name=f"Nickname", value=username.nick, inline=True)
        embed_.add_field(name=f"Created Date", value=f"<t:{int(time.mktime(username.created_at.timetuple()))}>", inline=False)
        embed_.add_field(name=f"Joined Date", value=f"<t:{int(time.mktime(username.joined_at.timetuple()))}>", inline=False)
        roles_out = []

        # create list with all roles. Note that first role in list always is @everyone
        for c_role in reversed(username.roles[1:]):
            roles_out.append(f"<@&{c_role.id}>")
        embed_.add_field(name=f"Roles", value=", ".join(roles_out), inline=False)
        await ctx.respond(embed=embed_, ephemeral=True)


def setup(bot):
    bot.add_cog(UserInfo(bot))
