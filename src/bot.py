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
        self._stop = False
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
                await message.delete()
                commands = self._commands.get_whole_file()
                inputMessage = str.split(str(message.content))
                inputMessage = str.replace(inputMessage[0], self._prefix, "")
                if message.content.startswith(f"{self._prefix}stop"):
                    if await self.is_user(message.author):
                        self._stop = True
                        embed = discord.Embed(description="Stopped mentioning!", color=0xb87328, title="Mention")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(f"{message.author.mention} you are not allowed to use that command!")
                elif message.content.startswith(f"{self._prefix}clear"):
                    if await self.is_admin(message.author):
                        msg = message.content
                        msg = str.replace(msg, "  ", " ")
                        msg = str.split(msg, " ")
                        if len(msg) == 2:
                            try:
                                await message.channel.purge(limit=int(msg[1]))
                                delmsg = await message.channel.send(f"Cleared last {msg[1]} messages!")
                                await asyncio.sleep(3)
                                await delmsg.delete()
                            except Exception:
                                pass
                        elif len(msg) == 3:
                            try:
                                identifier = msg[2]
                                identifier = str.replace(identifier, f" ", "")
                                identifier = str.replace(identifier, f"<", "")
                                identifier = str.replace(identifier, f">", "")
                                identifier = str.replace(identifier, f"@", "")
                                identifier = str.replace(identifier, f"!", "")
                                cuser = self._client.get_user(int(identifier))
                                await message.channel.purge(limit=int(msg[1]), check = lambda m: m.author.id == cuser.id)
                                delmsg = await message.channel.send(f"Cleared last {msg[1]} messages!")
                                await asyncio.sleep(3)
                                await delmsg.delete()
                            except Exception:
                                pass
                        else:
                            errorType = "Clear"
                            errorCommand = f"{message.author.mention} try to use {self._prefix}clear amount [@user]"
                            errorOccurred = True
                    else:
                        errorType = "Permissions"
                        errorCommand = f"You are not allowed to use this command!"
                        errorOccurred = True
                elif message.content.startswith(f"{self._prefix}poke"):
                    if await self.is_user(message.author):
                        msg = message.content
                        msg = str.replace(msg, "  ", " ")
                        msg = str.split(msg, " ")
                        if len(msg) != 1:
                            identifier = msg[1]
                            identifier = str.replace(identifier, f" ", "")
                            identifier = str.replace(identifier, f"<", "")
                            identifier = str.replace(identifier, f">", "")
                            identifier = str.replace(identifier, f"@", "")
                            identifier = str.replace(identifier, f"!", "")
                            try:
                                user = self._client.get_user(int(identifier))
                                if len(msg) == 3:
                                    for i in range(0, int(msg[2])):
                                        if self._stop:
                                            self._stop = False
                                            break
                                        await message.channel.send(user.mention)
                                        await asyncio.sleep(1)
                                elif len(msg) == 2:
                                    await message.channel.send(user.mention)
                                else:
                                    errorType = "Poke"
                                    errorCommand = f"Please use {self._prefix}poke @user [amount]"
                                    errorOccurred = True
                            except Exception as ex:
                                print(ex)
                                errorType = "Poke"
                                errorCommand = f"Please use {self._prefix}poke @user [amount]"
                                errorOccurred = True
                        else:
                            errorType = "Poke"
                            errorCommand = f"Please use {self._prefix}poke @user [amount]"
                            errorOccurred = True
                    else:
                        errorType = "Permissions"
                        errorCommand = f"You are not allowed to use this command!"
                        errorOccurred = True



                else: # use commands.json
                    try:
                        if commands[inputMessage] is not None:
                            if "<embed>" in commands[inputMessage]:
                                output = str.replace(commands[inputMessage], "<embed>", "")
                                embed = discord.Embed(description=output, color=0xb87328)
                                await message.channel.send(embed=embed)
                            else:
                                await message.channel.send(commands[inputMessage])
                    except Exception:
                        errorOccurred = True
                        errorCommand = f"Command '{inputMessage}' not found!"
                        errorType = "Command"
                if not errorOccurred:
                    self.print_log(f"[Commands] {message.author} used command '{inputMessage}'")
            if errorOccurred:
                await message.channel.send(errorCommand)
                self.print_log(f"[{errorType}] [{message.author}] {errorCommand}")

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

    async def is_admin(self, user):
        admins = Config("./src/config/admins.json").get_whole_file()
        if str(user.id) in admins.values():
            return True
        else:
            return False

    async def is_user(self, user):
        admins = Config("./src/config/admins.json").get_whole_file()
        users = Config("./src/config/users.json").get_whole_file()
        if str(user.id) in admins.values():
            return True
        elif str(user.id) in users.values():
            return True
        else:
            return False

    async def remove_role(self, user, role):
        await user.remove_roles(role, reason=f"Unlinked account with {str(user)}")

    def print_log(self, message):
        time = self.get_current_time()
        print(f"[{time}] {message}")
