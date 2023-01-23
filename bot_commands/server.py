import discord
from tools.functions import find_category, find_channel
import re
import tools.permissions as permissions
import asyncio
from bot_messages.help import help
from bot_messages.rules import rules


class Server():
    def __init__(self, interaction):
        self.interaction = interaction
        self.guild = interaction.guild
        self.role_assignment = None

    async def setup(self):
        print(f"[SERVER] Set up")
        await self.interaction.response.defer()
        await asyncio.sleep(1)

        '''if 'COMMUNITY' not in self.guild.features:  # doesnt work yet
            rules = await self.guild.create_text_channel(name='rules')
            announcements = await self.guild.create_text_channel(name='announcements')

            await self.guild.edit(rules_channel=rules, public_updates_channel=announcements)
            # discord.app_commands.errors.CommandInvokeError: Command 'server' raised an exception: Forbidden: 403 Forbidden (error code: 40006): This feature has been temporarily disabled'''

        for category in self.guild.categories:
            await category.delete()
            print(f"[SERVER] {category.name} deleted")

        # rules channel
        await self.guild.rules_channel.edit(position=1)
        print(f"[SERVER] rules_channel moved position 1")

        # announcements
        await self.guild.public_updates_channel.edit(position=2)
        print(f"[SERVER] announcements channel moved position 2")

        # bot-commands
        bot_channel = await self.guild.create_text_channel(name='bot commands', position=3)
        print(f"[SERVER] #bot-commands created on position 3")

        # General
        # General text
        # General voice
        # general channels
        general_text = discord.utils.get(self.guild.channels, name='general')
        general_voice = discord.utils.get(self.guild.channels, name='General')

        general_category = await self.guild.create_category(name='general chat', position=4)
        print(f"[SERVER] category #general-chat created on position 4")

        await general_text.edit(category=general_category)
        print("[SERVER] moved #general-text to #general-chat category")
        await general_voice.edit(category=general_category)
        print("[SERVER] moved #general-voice to #general-chat category")

        moderator = discord.utils.get(
            self.guild.channels, name='moderator-only')
        await moderator.edit(position=0)
        print(f"[SERVER] moderator channel moved position 0")

        # role-assignment channel
        overwrite_role = {self.guild.default_role: permissions.role_channel}
        self.role_assignment = await self.guild.create_text_channel(name='fandom role assignment', position=5, overwrites=overwrite_role)
        print(f"[SERVER] #fandom-role-assignment created on position 5")
        await self.role_assignment.send(f'Click on the emoji below the fandom you want to join to assign yourself the role.')
        print(f"[SERVER] Message sent on #fandom-role-assignment")

        # kpop-extravaganza
        # bot can create forum channels
        kpop_channel = await self.guild.create_category(name='kpop extravaganza', position=6)
        print("[SERVER] #kpop-extravaganza created on position 6")

        # post message on rules
        message = rules(self.guild, bot_channel, self.role_assignment,
                        general_category, general_text, general_voice, kpop_channel)
        await self.guild.rules_channel.send(message)
        print(f'[SERVER] Message sent on #rules')

        # respond to the command
        await self.interaction.followup.send(f'The server has been configured. Visit {self.guild.rules_channel.mention} for more informations.')

    async def create_forum(self, name):
        kpop_cat = find_category(self.interaction, 'kpop extravaganza')
        return await self.guild.create_forum(name=f'{name}', category=kpop_cat)
        print(f"[FORUM] {name} created")

    async def create_fandom(self, name, emoji, hex_color):
        forum = await self.create_forum(name)

        # check the hex color value
        if '#' not in hex_color:
            hex_color = f'#{hex_color}'
        colour = discord.Colour.from_str(hex_color)

        fandom_role = await self.guild.create_role(name=name, colour=colour)
        print(f"[FANDOM] {name} role created")

        role_channel = discord.utils.get(
            self.guild.channels, name='fandom-role-assignment')
        fandom_message = await role_channel.send(name)
        print(f"[FANDOM] {name} posted in #fandom-role-assignment")
        await fandom_message.add_reaction(emoji)
        print(f"[FANDOM] reaction added")

        # type:ignore
        await self.interaction.response.defer()
        await asyncio.sleep(2)
        await self.interaction.followup.send(f'The fandom {name} has been created! You can now use the {forum.mention} forum and also attribute yourself the {name} role in {role_channel.mention} by clicking on the emoji under {name}')
        print(f"[FANDOM] Message send back")

    async def help_command(self):
        role_assignment = find_channel(
            self.interaction.guild, "fandom-role-assignment")

        message = help(role_assignment)
        await self.interaction.response.send_message(message)
        print(f"[HELP] Help message send back")
