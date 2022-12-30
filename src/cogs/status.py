import discord
import requests
from discord.ext import commands, tasks
import betteruptime
from decouple import config
from src.db import DB
import os


class Status(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.db = DB()
        self.update_service_status.start()
        token = config("BETTERUPTIME_TOKEN", default=None)
        if token:
            self.client = betteruptime.Client(bearer_token=token)
            self.configured = True
        else:
            self.configured = False

    def get_betteruptime_status(self):
        section_names = {} # dictionary with the id of the section and name
        sections_with_status = {}

        status_pages = self.client.status_pages.list()

        if "data" in status_pages:
            status_pages = status_pages["data"]
            status_page_id = status_pages[0]["id"]
            status_pages_sections = self.client.status_pages(status_page_id).sections.list() # swap section ID
            entity_status = {} # status of entity id
            for c_monitor in self.client.monitors.list()["data"]:
                entity_status[c_monitor["id"]] = c_monitor["attributes"]["status"]
            for c_heartbeat in self.client.heartbeats.list()["data"]:
                entity_status[c_heartbeat["id"]] = c_heartbeat["attributes"]["status"]

            # get section_names dictionary
            if "data" in status_pages_sections:
                status_pages_sections = status_pages_sections["data"]
                for c_status_page_section in status_pages_sections:
                    section_names[c_status_page_section["id"]] = c_status_page_section["attributes"]["name"]
                    sections_with_status[c_status_page_section["attributes"]["name"]] = []

            # get status_page_resources
            # status_page_
            status_page_resources = self.client.status_pages(status_page_id).resources.list()
            if "data" in status_page_resources:
                status_page_resources = status_page_resources["data"]
                for c_status_page_resource in status_page_resources:
                    name = c_status_page_resource["attributes"]["public_name"]
                    section_name = section_names[str(c_status_page_resource["attributes"]["status_page_section_id"])]
                    status = entity_status[str(c_status_page_resource["attributes"]["resource_id"])]
                    sections_with_status[section_name].append({"name": name, "status": status})

        return sections_with_status

    def get_betteruptime_site_title(self):
        status_pages = self.client.status_pages.list()
        if "data" in status_pages:
            status_pages = status_pages["data"]
            return status_pages[0]["attributes"]["custom_domain"]

    @tasks.loop(minutes=5)
    async def update_service_status(self):
        url = config("BETTERUPTIME_HEARTBEAT_URL")
        if url != "":
            requests.get(url)
        else:
            print("BETTERUPTIME_HEARTBEAT_URL not set!")
            os._exit(-1)

    @discord.slash_command(name="status", description="Get service status of all services!")
    async def service_status(self, ctx: discord.commands.context.ApplicationContext):
        if ctx.author.guild_permissions.administrator or self.db.is_moderator(ctx.guild_id, ctx.author.id):
            if self.configured:
                site_title = self.get_betteruptime_site_title()
                embed_ = discord.Embed(title=f"{site_title}", color=0xb87328)
                services = self.get_betteruptime_status()
                for c_category_name in services:
                    category_list = []
                    for c_service in services[c_category_name]:
                        category_list.append(f"{c_service['name']}: {c_service['status']}")
                    embed_.add_field(name=f"{c_category_name}", value="\n".join(category_list), inline=False)
                await ctx.respond(embed=embed_)
            else:
                await ctx.respond("BetterUptime integration is not configured correctly!", delete_after=5)
        else:
            await ctx.respond(f"Sorry, but you don't have enough permissions!", delete_after=5)


def setup(bot):
    bot.add_cog(Status(bot))
