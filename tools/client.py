import discord
from bot_commands.env import Env
from tools.bot_intents import intents


class aClient(discord.Client):
    def __init__(self, tree):
        super().__init__(intents=intents)
        self.synced = False
        self.tree = tree

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()  # type:ignore
            self.synced = True
        print(f'We have logged in as {self.user}')

    async def on_member_join(self, member):
        await Env(member=member).join()

    async def on_member_remove(self, member):
        await Env(member=member).leave()

    async def on_message(self, message):
        await Env(message=message).latest_msg()
