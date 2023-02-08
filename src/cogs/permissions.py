import discord
import requests
from discord.ext import commands
from src.models import User
from src.bot import db
from discord import guild_only


class Permissions(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.db = db

    @guild_only()
    @discord.slash_command(name="addmod", description="Add a Moderator!")
    async def addmod(self, ctx: discord.commands.context.ApplicationContext,
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True)):
        if ctx.author.guild_permissions.administrator or self.db.is_admin(ctx.guild_id, ctx.author.id):
            user = self.db.update_or_add_user_to_guild(ctx.guild_id, username.id, User(moderator=True))
            if user:
                await ctx.respond(f"<@{username.id}> is now a Moderator!")
            else:
                await ctx.respond(f"An error occurred while adding <@{username.id}> to Moderators!")
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)

    @guild_only()
    @discord.slash_command(name="delmod", description="Remove a Moderator!")
    async def delmod(self, ctx: discord.commands.context.ApplicationContext,
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True)):
        if ctx.author.guild_permissions.administrator or self.db.is_admin(ctx.guild_id, ctx.author.id):
            user = self.db.update_or_add_user_to_guild(ctx.guild_id, username.id, User(moderator=False))
            if user:
                await ctx.respond(f"<@{username.id}> is no longer a Moderator!")
            else:
                await ctx.respond(f"An error occurred while removing <@{username.id}> from Moderators!")
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)

    @guild_only()
    @discord.slash_command(name="addadmin", description="Add an Administrator!")
    async def addadmin(self, ctx: discord.commands.context.ApplicationContext,
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True)):
        if ctx.author.guild_permissions.administrator or self.db.is_admin(ctx.guild_id, ctx.author.id):
            user = self.db.update_or_add_user_to_guild(ctx.guild_id, username.id, User(administrator=True))
            if user:
                await ctx.respond(f"<@{username.id}> is now an Administrator!")
            else:
                await ctx.respond(f"An error occurred while adding <@{username.id}> to Administrators!")
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)

    @guild_only()
    @discord.slash_command(name="deladmin", description="Remove an Administrator!")
    async def deladmin(self, ctx: discord.commands.context.ApplicationContext,
                    username: discord.Option(discord.SlashCommandOptionType.user, "username", required=True)):
        if ctx.author.guild_permissions.administrator or self.db.is_admin(ctx.guild_id, ctx.author.id):
            user = self.db.update_or_add_user_to_guild(ctx.guild_id, username.id, User(administrator=False))
            if user:
                await ctx.respond(f"<@{username.id}> is no longer an Administrator!")
            else:
                await ctx.respond(f"An error occurred while removing <@{username.id}> from Administrator!")
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)

    @guild_only()
    @discord.slash_command(name="permissions", description="List permissions!")
    async def permissions(self, ctx: discord.commands.context.ApplicationContext,
                       username: discord.Option(discord.SlashCommandOptionType.user, "username", required=False)):
        if ctx.author.guild_permissions.administrator or self.db.is_moderator(ctx.guild_id, ctx.author.id):
            if username:
                embed_ = discord.Embed(title=f"Permissions of {username.name}", color=0xb87328)
                embed_.add_field(name="Moderator", value=self.db.is_moderator(ctx.guild_id, username.id))
                embed_.add_field(name="Administrator", value=self.db.is_admin(ctx.guild_id, username.id))
                # user-specific permissions
                await ctx.respond(embed=embed_, ephemeral=True)
            else:
                embed_ = discord.Embed(title=f"Permissions list", color=0xb87328)
                moderators = []
                administrators = []
                guild = self.db.get_guild_by_id(ctx.guild_id)
                for c_user in guild.users:
                    user_obj = await self.bot.fetch_user(c_user.id)
                    name = f"<@{user_obj.id}>"
                    if c_user.administrator:
                        administrators.append(name)
                    if c_user.moderator:
                        moderators.append(name)
                moderator_out = "None"
                administrator_out = "None"
                if len(moderators) != 0:
                    moderator_out = "\n".join(moderators)
                if len(administrators) != 0:
                    administrator_out = "\n".join(administrators)
                embed_.add_field(name="Moderators", value=moderator_out)
                embed_.add_field(name="Administrators", value=administrator_out)
                await ctx.respond(embed=embed_, ephemeral=True)
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", ephemeral=True)


def setup(bot):
    bot.add_cog(Permissions(bot))