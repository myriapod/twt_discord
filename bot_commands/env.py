import discord
from tools.functions import create_env, get_member_roles


class Env():
    def __init__(self, member=discord.Member, message=discord.Message):
        self.member = member
        self.message = message

    async def join(self):
        """
        Set up the environment for the new user when they join
        """
        print(f'{self.member.name} has joined the server!')
        await create_env(self.member)

    async def leave(self):
        """
        When a user leaves, their channels and roles get deleted
        Some of it should be optional for optimisation
        """
        print(f'{self.member.name} has left.')

        # deletes all the roles (personal and follower)
        roles = get_member_roles(self.member)
        for role in roles:
            await role.delete()

        # for the test phase mostly - delete channels
        channel_list = self.member.guild.by_category()
        for channel in channel_list:
            category = channel[0]
            if category and self.member.name in category.name:
                await category.delete()
                for chan in channel[1]:
                    await chan.delete()
        print(f'The environment for {self.member.name} has been removed.')

    async def latest_msg(self):
        """
        sort the categories from latest activity to oldest activity
        """
        new_category = self.message.channel.category
        if new_category and "zone" in new_category.name:
            await new_category.edit(position=2)
            print(f'Category {new_category.name} moved to the top')
        elif new_category:
            await self.message.channel.parent.edit(position=0)
            print(f'Forum {self.message.channel.parent} moved to the top')
