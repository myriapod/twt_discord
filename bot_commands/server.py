import discord
from tools.functions import find_category
import re


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

        # rules
        # > add a server map message in there
        # should consider creating it but for now discord isnt letting that be possible so just the positions in the channel list
        await self.guild.rules_channel.edit(position=1)

        # announcements
        await self.guild.public_updates_channel.edit(position=2)

        # bot-commands
        bot_channel = await self.guild.create_text_channel(name='bot commands', position=3)

        # General
        # General text
        # General voice
        general_category = await self.guild.create_category(name='general chat', position=4)

        for channel in self.guild.channels:
            if re.match('G|general$', channel.name):
                await channel.edit(category=general_category)
            elif re.match('moderator-only', channel.name):
                await channel.edit(position=0)

        # kpop-extravaganza
        # bot can create forum channels
        kpop_channel = await self.guild.create_category(name='kpop extravaganza', position=5)

        # personal channels
        general_text = discord.utils.get(self.guild.channels, name='general')
        general_voice = discord.utils.get(self.guild.channels, name='General')
        # post message on rules
        message = f'''
Welcome to the {self.guild.name} server!

This is the server map that will help guide you through the server.

{bot_channel.mention} is where you can use the bot and its / commands.

**{general_category.mention}** is the general text ({general_text.mention}) and voice chat ({general_voice.mention}) that everyone in the server has access to.

**{kpop_channel.mention}** is a semi-organized place that everyone can access. There are forums dedicated to certain bands/topics that users can create using the bot command `/forum`.

The rest of the server is **personal categories** that can be accessed by others through the `/follow` command.
Only the personal category owner can make new forum posts, but all of their followers can respond to a post, as well as post in the text channel.
You should have full control and access over your personal category (ie. feel free to create or delete channels...)
        '''
        await self.guild.rules_channel.send(message)

        await self.interaction.message.send('The server has been configured.')

    async def create_forum(self, name):
        kpop_cat = find_category(self.interaction, 'kpop extravaganza')
        await self.guild.create_forum(name=f'{name}', category=kpop_cat)
