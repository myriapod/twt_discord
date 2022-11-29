import discord
from discord import app_commands
from discord.ext import commands
from commands.catchup import Follow, NSFW, CatchUp, Env
import bot_intents

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