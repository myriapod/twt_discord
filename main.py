import discord
from discord import app_commands
from discord.ext import commands

import os
from dotenv import load_dotenv

from bot_commands.catchup import CatchUp
from bot_commands.env import Env
from bot_commands.follow import Follow
from bot_commands.mdni import NSFW
from bot_commands.server import Server

import tools.bot_intents as bot_intents

load_dotenv()

token = os.getenv('TWT_DISCORD_API_KEY')

intents = bot_intents.intents


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'We have logged in as {self.user}')

    async def on_member_join(self, member):
        await Env(member=member).join()

    async def on_member_remove(self, member):
        await Env(member=member).leave()

    async def on_message(self, message):
        await Env(message=message).latest_msg()


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name="follow", description="Follow a user")
async def follow_user(interaction: discord.Interaction, name: discord.User):
    await Follow(interaction, interaction.user, name).follow()


@tree.command(name="unfollow", description="Unfollow a user")
async def unfollow_user(interaction: discord.Interaction, name: discord.User):
    await Follow(interaction, interaction.user, name).unfollow()


@tree.command(name="mdni", description="Make your personal channels age restricted")
async def nsfw_category(interaction: discord.Interaction):
    await NSFW(interaction, interaction.user).mdni()


@tree.command(name="make_follow", description="Make a user follow another")
@commands.has_permissions(administrator=True)
async def make_follow(interaction: discord.Interaction, follower: discord.User, followee: discord.User):
    await Follow(interaction, follower=follower, target=followee).follow()


@tree.command(name="catchup", description="Creates environment that weren't setup while the bot was offline")
async def catch_up(interaction: discord.Interaction, mode: str):
    catchup = CatchUp(interaction)
    if mode == "auto":
        await catchup.auto()
    elif mode == "manual":
        await catchup.manual()


@tree.command(name="forum", description="Creates a forum for the entered band name under the category #kpop-extravaganza")
async def create_forum(interaction: discord.Interaction, name: str):
    await Server(interaction).create_forum(name)


@tree.command(name="server", description="Sets up the server with certain categories and features")
@commands.has_permissions(administrator=True)
async def server_set_up(interaction: discord.Interaction):
    await Server(interaction).setup()

try:
    client.run(token)
except:
    print('Missing token. Please fill in the token variable in the .env file.')
