import discord
from discord import app_commands
from discord.ext import commands
from botcommands import Follow, NSFW, CatchUp, Env
import bot_intents

token = ""


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
async def catch_up(interaction: discord.Interaction, message: str):
    catchup = CatchUp(interaction)
    if message == "auto":
        await catchup.auto()
    elif message == "manual":
        await catchup.manual()


client.run(token)
