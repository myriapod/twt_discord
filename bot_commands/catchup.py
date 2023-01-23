from tools.functions import create_env, manual_env
import asyncio


class CatchUp():

    """
    Command to catchup with server newcommers while the bot was offline
    """

    def __init__(self, interaction):
        self.interaction = interaction

    async def auto(self):
        print('[CATCH UP] [AUTO] Catching up while the bot was gone...')
        for member in self.interaction.guild.members:
            if len(member.roles) == 1:
                print(f'[CATCH UP] [AUTO] {member.name} is a new member')
                await create_env(member)
        await self.interaction.response.defer()
        await asyncio.sleep(5)
        await self.interaction.followup.send('All caught up!')
        print('[CATCH UP] [AUTO] The bot is caught up.')

    async def manual(self):
        print("[CATCH UP] [MANUAL] Looking for users without environments...")
        for member in self.interaction.guild.members:
            env = False
            for channel in self.interaction.guild.categories:
                if member.name in channel.name:
                    env = True
            if not env:
                print(f'[CATCH UP] [MANUAL] {member.name} is a new member')
                await manual_env(self.interaction, member)
        await self.interaction.response.defer()
        await asyncio.sleep(5)
        await self.interaction.followup.send('All caught up!')
        print('[CATCH UP] [MANUAL] The bot is caught up.')
