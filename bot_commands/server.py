import discord
from tools.functions import find_category
import re
import tools.permissions as permissions


class Server():
    def __init__(self, interaction):
        self.interaction = interaction
        self.guild = interaction.guild

    async def setup(self):
        if 'COMMUNITY' not in self.guild.features:  # doesnt work yet
            rules = await self.guild.create_text_channel(name='rules')
            announcements = await self.guild.create_text_channel(name='announcements')

            await self.guild.edit(community=True, rules_channel=rules, public_updates_channel=announcements)
            # discord.app_commands.errors.CommandInvokeError: Command 'server' raised an exception: Forbidden: 403 Forbidden (error code: 40006): This feature has been temporarily disabled

        for category in self.guild.categories:
            await category.delete()

        # rules channel
        await self.guild.rules_channel.edit(position=1)

        # announcements
        await self.guild.public_updates_channel.edit(position=2)

        # bot-commands
        bot_channel = await self.guild.create_text_channel(name='bot commands', position=3)

        # General
        # General text
        # General voice
        # general channels
        general_text = discord.utils.get(self.guild.channels, name='general')
        general_voice = discord.utils.get(self.guild.channels, name='General')

        general_category = await self.guild.create_category(name='general chat', position=4)

        await general_text.edit(category=general_category)  # type:ignore
        await general_voice.edit(category=general_category)  # type:ignore

        moderator = discord.utils.get(
            self.guild.channels, name='moderator-only')
        await moderator.edit(position=0)  # type:ignore

        # role-assignment channel
        overwrite_role = {self.guild.default_role: permissions.role_channel}
        role_assignment = await self.guild.create_text_channel(name='fandom role assignment', position=5, overwrites=overwrite_role)
        await role_assignment.send(f'Click on the emoji below the fandom you want to join to assign yourself the role.')

        # kpop-extravaganza
        # bot can create forum channels
        kpop_channel = await self.guild.create_category(name='kpop extravaganza', position=6)

        # post message on rules
        message = f'''
Welcome to the {self.guild.name} server!

This is the server map that will help guide you through the server.

{bot_channel.mention} is where you can use the bot and its / commands.

**{general_category.mention}** is the general text ({general_text.mention}) and voice chat ({general_voice.mention}) that everyone in the server has access to.

{role_assignment.mention} is a channel where you can assign yourself fandom roles. They are purely for cosmetic purposes and don't bring special access to any of the fandom forums as they are accessible to everyone on the server by default.

**{kpop_channel.mention}** is a semi-organized place that everyone can access. There are forums dedicated to certain bands/topics that users can create using the bot command `/forum`.

The rest of the server is **personal categories** that can be accessed by others through the `/follow` command.
Only the personal category owner can make new forum posts, but all of their followers can respond to a post, as well as post in the text channel.
You should have full control and access over your personal category (ie. feel free to create or delete channels...)
        '''
        await self.guild.rules_channel.send(message)

        # respond to the command
        await self.interaction.response.send_message(f'The server has been configured. Visit {self.guild.rules_channel.mention} for more informations.')

    async def create_forum(self, name):
        kpop_cat = find_category(self.interaction, 'kpop extravaganza')
        return await self.guild.create_forum(name=f'{name}', category=kpop_cat)

    async def create_fandom(self, name, emoji, hex_color):
        forum = await self.create_forum(name)

        # check the hex color value
        if '#' not in hex_color:
            hex_color = f'#{hex_color}'
        colour = discord.Colour.from_str(hex_color)

        fandom_role = await self.guild.create_role(name=name, colour=colour)

        role_channel = discord.utils.get(
            self.guild.channels, name='fandom-role-assignment')
        fandom_message = await role_channel.send(name)
        await fandom_message.add_reaction(emoji)

        # type:ignore
        await self.interaction.response.send_message(f'The fandom {name} has been created! You can now use the {forum.mention} forum and also attribute yourself the {name} role in {role_channel.mention} by clicking on the emoji under {name}')
