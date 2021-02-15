from src.db import Config
import discord
import asyncio
import time
from datetime import datetime
from discord.utils import get
import threading


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
                        embed = discord.Embed(description="Stopped mentioning!", color=0xb87328)
                        delmsg = await message.channel.send(embed=embed)
                        await asyncio.sleep(5)
                        await delmsg.delete()
                    else:
                        errorType = "Permissions"
                        errorCommand = f"You are not allowed to use this command!"
                        errorOccurred = True
                elif message.content.startswith(f"{self._prefix}setup"):
                    if await self.is_admin(message.author):
                        if await self.check_role(message.author, self._config.read_config_file("user_role")):
                            await message.channel.send("Updated all channels!")
                            await self.check_mute_role_channels(message.author)
                        else:
                            await message.author.guild.create_role(name=self._config.read_config_file("user_role"))
                            await self.check_mute_role_channels(message.author)
                            await message.channel.send(f"Added role {self._config.read_config_file('user_role')} to server!")
                elif message.content.startswith(f"{self._prefix}unmute"):
                    if await self.is_admin(message.author, check_file=False):
                        msg = message.content
                        msg = str.replace(msg, "  ", " ")
                        msg = str.split(msg, " ")
                        if len(msg) == 2:
                            try:
                                identifier = msg[1]
                                identifier = str.replace(identifier, f" ", "")
                                identifier = str.replace(identifier, f"<", "")
                                identifier = str.replace(identifier, f">", "")
                                identifier = str.replace(identifier, f"@", "")
                                identifier = str.replace(identifier, f"!", "")
                                user = self._client.get_user(int(identifier))
                                role = get(message.author.guild.roles, name=self._config.read_config_file("mute_role"))
                                member = message.author.guild.get_member(int(identifier))
                                try:
                                    await member.edit(mute=False)
                                except Exception:
                                    pass
                                await member.remove_roles(role)
                                delmsg = await message.channel.send(f"Successfully unmuted {user.mention}!")
                                await asyncio.sleep(5)
                                await delmsg.delete()
                            except Exception as ex:
                                print(ex)
                                errorType = "Error"
                                errorCommand = f"Something went wrong!"
                                errorOccurred = True
                        else:
                            errorType = "Unute"
                            errorCommand = f"{message.author.mention} try to use {self._prefix}unmute @user"
                            errorOccurred = True
                elif message.content.startswith(f"{self._prefix}mute"):
                    #await message.channel.send("mute!")
                    if await self.is_admin(message.author, check_file=False):
                        loop = asyncio.get_event_loop()
                        x = threading.Thread(target=asyncio.run_coroutine_threadsafe, args=(self.check_mute_role_channels(message.author),loop,))
                        x.start()
                        #await self.check_mute_role_channels(message.author)
                        msg = message.content
                        msg = str.replace(msg, "  ", " ")
                        msg = str.split(msg, " ")
                        if len(msg) == 2:
                            try:
                                identifier = msg[1]
                                identifier = str.replace(identifier, f" ", "")
                                identifier = str.replace(identifier, f"<", "")
                                identifier = str.replace(identifier, f">", "")
                                identifier = str.replace(identifier, f"@", "")
                                identifier = str.replace(identifier, f"!", "")
                                user = self._client.get_user(int(identifier))
                                if not message.author == user:
                                    role = get(message.author.guild.roles, name=self._config.read_config_file("mute_role"))
                                    member = message.author.guild.get_member(int(identifier))
                                    try:
                                        await member.edit(mute=True)
                                    except Exception:
                                        pass
                                    await member.add_roles(role)
                                    delmsg = await message.channel.send(f"Successfully muted {user.mention}!")
                                    await asyncio.sleep(5)
                                    await delmsg.delete()
                                else:
                                    errorType = "Mute"
                                    errorCommand = f"You cannot mute yourself!"
                                    errorOccurred = True
                            except Exception as ex:
                                print(ex)
                                errorType = "Error"
                                errorCommand = f"Something went wrong!"
                                errorOccurred = True
                        else:
                            errorType = "Mute"
                            errorCommand = f"{message.author.mention} try to use {self._prefix}mute @user"
                            errorOccurred = True
                    else:
                        errorType = "Permissions"
                        errorCommand = f"You are not allowed to use this command!"
                        errorOccurred = True
                elif message.content.startswith(f"{self._prefix}clear"):
                    if await self.is_admin(message.author):
                        msg = message.content
                        msg = str.replace(msg, "  ", " ")
                        msg = str.split(msg, " ")
                        if len(msg) == 2:
                            try:
                                loop = asyncio.get_event_loop()
                                x = threading.Thread(target=asyncio.run_coroutine_threadsafe, args=(self.purge_messages(message, int(msg[1])), loop,))
                                x.start()
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
                                loop = asyncio.get_event_loop()
                                # await message.channel.purge(limit=int(msg[1]), check=lambda m: m.author.id == cuser.id)
                                thread = threading.Thread(target=asyncio.run_coroutine_threadsafe, args=(self.purge_messages(message, int(msg[1]), cuser), loop,))
                                thread.start()
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
                        self._stop = False
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



                else:  # use commands.json
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
                delmsg = await message.channel.send(errorCommand)
                await asyncio.sleep(15)
                await delmsg.delete()
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

    async def is_admin(self, user, check_server=True, check_file=True):
        admins = Config("./src/config/admins.json").get_whole_file()
        if str(user.id) in admins.values() and check_file:
            return True
        elif check_server and user.guild_permissions.administrator:
            return True
        else:
            return False

    async def check_role(self, user, rolename):
        if get(user.guild.roles, name=rolename):
            return True
        else:
            return False

    async def is_user(self, user, use_role=True):
        has_role = None
        try:
            role = discord.utils.find(lambda r: r.name == self._config.read_config_file("user_role"), user.guild.roles)
            if role in user.roles:
                has_role = True
            else:
                has_role = False
        except Exception as ex:
            has_role = False
        admins = Config("./src/config/admins.json").get_whole_file()
        users = Config("./src/config/users.json").get_whole_file()
        if str(user.id) in admins.values():
            return True
        elif str(user.id) in users.values():
            return True
        elif use_role and has_role:
            return True
        else:
            return False

    async def remove_role(self, user, role):
        await user.remove_roles(role, reason=f"Unlinked account with {str(user)}")

    def print_log(self, message):
        time = self.get_current_time()
        print(f"[{time}] {message}")

    async def check_mute_role_channels(self, user):
        try:
            if not get(user.guild.roles, name=self._config.read_config_file("mute_role")):
                await user.guild.create_role(name=self._config.read_config_file("mute_role"))
            for channel in user.guild.channels:
                role = get(user.guild.roles, name=self._config.read_config_file("mute_role"))
                await channel.set_permissions(role, send_messages=False, speak=False)
            return True
        except Exception as ex:
            print(ex)
            return False

    async def purge_messages(self, message, amount, user=None):
        if amount > 20:
            delmsg = await message.channel.send(f"Clearing {amount} messages! This might take a while...")
            await asyncio.sleep(3)
            await delmsg.delete()
        if not user:
            await message.channel.purge(limit=amount)
        else:
            await message.channel.purge(limit=int(amount), check=lambda m: m.author.id == user.id)
        delmsg2 = await message.channel.send(f"Cleared last {amount} messages!")
        await asyncio.sleep(10)
        await delmsg2.delete()