from tools.functions import create_env, manual_env
import asyncio


class CatchUp():

    """
    Command to catchup with server newcommers while the bot was offline
    """

    def __init__(self, interaction):
        self.interaction = interaction

    async def auto(self):
        print(f'Catching up while the bot was gone...')
        for member in self.interaction.guild.members:
            if len(member.roles) == 1:
                print(f'> {member.name} is a new member')
                await create_env(member)
        print(f'Done!')
        await self.interaction.response.defer()
        await asyncio.sleep(5)
        await self.interaction.followup.send('All caught up!')

    async def manual(self):
        print("Looking for users without environments...")
        for member in self.interaction.guild.members:
            env = False
            for channel in self.interaction.guild.categories:
                if member.name in channel.name:
                    env = True
            if not env:
                await manual_env(self.interaction, member)
        print(f'Done!')
        await self.interaction.response.defer()
        await asyncio.sleep(5)
        await self.interaction.followup.send('All caught up!')
