import discord
from discord import app_commands
from discord.ext import commands

import os

from bot_commands.catchup import CatchUp
from bot_commands.env import Env
from bot_commands.follow import Follow
from bot_commands.mdni import NSFW
from bot_commands.server import Server
from bot_commands.fandom import Fandom

from tools.bot_intents import intents

token = os.environ.get('TWT_DISCORD_API_KEY')

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.role_channel = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'[LOG IN] We have logged in as {self.user}')

    async def on_member_join(self, member):
        # Sending a DM to the members when they join:
        # not used for now
        # channel = await member.create_dm()
        # welcome = open('bot_messages/welcome.txt', 'r', encoding='utf-8')
        # await channel.send(welcome.read())
        await Env(member=member).join()

    async def on_member_remove(self, member):
        await Env(member=member).leave()

    async def on_message(self, message):
        if message.channel.type != discord.ChannelType.private:
            await Env(message=message).latest_msg()

    async def on_raw_reaction_add(self, reaction):
        guild = self.get_guild(reaction.guild_id)
        reaction_channel = discord.utils.get(
            guild.channels, name="fandom-role-assignment")  # type:ignore

        if reaction.user_id != self.user.id:  # type:ignore
            if reaction.channel_id == reaction_channel.id:  # type:ignore
                await Fandom(reaction=reaction).assign_fandom(reaction_channel=reaction_channel)

            # add a dm 'youve joined the xx fandom?'


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name="follow", description="Follow a user")
async def follow_user(interaction: discord.Interaction, name: discord.User):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await Follow(interaction, interaction.user, name).follow()


@tree.command(name="unfollow", description="Unfollow a user")
async def unfollow_user(interaction: discord.Interaction, name: discord.User):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await Follow(interaction, interaction.user, name).unfollow()


@tree.command(name="mdni", description="Make your personal category age restricted")
async def nsfw_category(interaction: discord.Interaction):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await NSFW(interaction, interaction.user).mdni()


@tree.command(name="make_follow", description="Make a user follow another")
@commands.has_permissions(administrator=True)
async def make_follow(interaction: discord.Interaction, follower: discord.User, followee: discord.User):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await Follow(interaction, follower=follower, target=followee).follow()


@tree.command(name="catchup", description="Creates environments that weren't setup while the bot was offline")
@commands.has_permissions(administrator=True)
async def catch_up(interaction: discord.Interaction, mode: str):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        catchup = CatchUp(interaction)
        if mode == "auto":
            await catchup.auto()
        elif mode == "manual":
            await catchup.manual()


@tree.command(name="fandom", description="Creates a fandom")
async def create_forum(interaction: discord.Interaction, name: str, emoji: str, hex_color: str):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await Server(interaction).create_fandom(name, emoji, hex_color)


@tree.command(name="server", description="Sets up the server")
@commands.has_permissions(administrator=True)
async def server_set_up(interaction: discord.Interaction):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message('This command can only be used in the server.')
    else:
        await Server(interaction).setup()


@tree.command(name="help", description="Help for the supported commands")
async def help_command(interaction: discord.Interaction):
    if interaction.channel.type == discord.ChannelType.private:
        await interaction.response.send_message(f'''
List of available commands:
- `/help` : displays this message
- `/follow [user to follow]` : grants you access to the personal channels of the person you want to follow
- `/unfollow [person to unfollow]` : removes the access to the personal channels of the person you want to unfollow
- `/mdni` : puts an age restriction on your personal channels
- `/fandom [name] [emoji] [hex color]` : creates a dedicated forum (accessible to everyone) and colored role that you can assign yourself in the #fandom-role-assignement channel
        ''')
    else:
        await Server(interaction).help_command()

try:
    client.run(token)  # type:ignore
except:
    print('[LOG IN] [ERROR] Missing token. Please fill in the token variable in the .env file.')