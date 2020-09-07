from src.db import Config
import discord
import asyncio
import time
from datetime import datetime


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
            self.print_log('[Status] We have logged in as {0.user}'.format(self._client))

        @self._client.event
        async def on_message(message):
            errorOccurred = False
            errorCommand = "An Error occurred."
            errorType = "Generic"
            if message.content.startswith(f"{self._prefix}"):
                commands = self._commands.get_whole_file()
                inputMessage = str.split(str(message.content))
                inputMessage = str.replace(inputMessage[0], self._prefix, "")
                try:
                    if commands[inputMessage] is not None:
                        if "<embed>" in commands[inputMessage]:
                            output = str.replace(commands[inputMessage], "<embed>", "")
                            embed = discord.Embed(description=output, color=0xb87328)
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(commands[inputMessage])
                        self.print_log(f"[Commands] {message.author} used command '{inputMessage}'")
                except Exception:
                    errorOccurred = True
                    errorCommand = f"Command '{inputMessage}' not found!"
                    errorType = "Command"
            if errorOccurred:
                await message.channel.send(errorCommand)
                self.print_log(f"[{errorType}] {errorCommand}")

        if self._config.read_config_file("enable_join_notification") == "True":
            @self._client.event
            async def on_member_join(member):
                message = self._config.read_config_file("join_notification")
                message = str.replace(message, "<user>", str(member))
                await member.send(message)

    async def add_role(self, user, role):
        await user.add_roles(role, reason=f"Linked account with {str(user)}")

    def get_current_time(self):
        now = datetime.now()
        output_time = '{0:%H:%M:%S}'.format(now)
        return output_time

    async def remove_role(self, user, role):
        await user.remove_roles(role, reason=f"Unlinked account with {str(user)}")

    def print_log(self, message):
        time = self.get_current_time()
        print(f"[{time}] {message}")