from src.db import Config
import discord
import asyncio


class Bot:
    def __init__(self, token, prefix="."):
        self._config = Config()
        self._commands = Config("./src/config/commands.json")
        self._client = discord.Client()
        self._prefix = prefix
        self.event_loader()
        self._client.run(token)

    def event_loader(self):
        @self._client.event
        async def on_ready():
            presence = self._config.read_config_file("status_message")
            presence = str.replace(presence, "<prefix>", self._prefix)
            await self._client.change_presence(activity=discord.Game(name=presence))
            print('[Status] We have logged in as {0.user}'.format(self._client))

        @self._client.event
        async def on_message(message):
            if message.content.startswith(f"{self._prefix}ping"):
                await message.channel.send(self._commands.read_config_file("ping"))
            if message.content.startswith(f"{self._prefix}help"):
                await message.channel.send(self._commands.read_config_file("help"))

        if self._config.read_config_file("enable_join_notification") == "True":
            @self._client.event
            async def on_member_join(member):
                message = self._config.read_config_file("join_notification")
                message = str.replace(message, "<user>", str(member))
                await member.send(message)

    async def add_role(self, user, role):
        await user.add_roles(role, reason=f"Linked account with {str(user)}")

    async def remove_role(self, user, role):
        await user.remove_roles(role, reason=f"Unlinked account with {str(user)}")

