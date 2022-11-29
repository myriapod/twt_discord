import discord
from functions import create_env, manual_env, get_member_roles


class Follow():
    def __init__(self, interaction, follower, target):
        self.interaction = interaction
        self.follower = follower
        self.target = target

    async def follow(self):
        r_name = f'{self.target.name}-follower'

        # values to make the bot verbose
        already_following = False

        for role in self.interaction.guild.roles:
            if role.name == r_name:
                # check to see if the member isn't already following the requested user
                for m_role in self.follower.roles:
                    if role == m_role:
                        print(
                            f'{self.follower.name} is already following {self.target.name}')
                        await self.interaction.response.send_message(f'{self.follower.name} is already following {self.target.name}')
                        already_following = True

                if not already_following:
                    await self.follower.add_roles(role)
                    print(
                        f'{self.follower.name} is now following {self.target.name}')
                    await self.interaction.response.send_message(f'{self.follower.mention} is now following {self.target.mention}')

    async def unfollow(self):
        """
        Similar to follow but in reverse

        Bot command to call with !unfollow
        De-assigns the role username-follower to the member requesting

        member = person sending in the request
        user = person to follow

        NOT VERBOSE (on purpose)

        Improvement possible: if we(the team of me and i) get this bot to work in dms, you could request privately to unfollow someone
        """

        r_name = f'{self.target.name}-follower'
        for role in self.interaction.guild.roles:
            if role.name == r_name:
                for m_role in self.follower.roles:
                    if role == m_role:
                        await self.follower.remove_roles(role)
                        print(
                            f'{self.follower.name} has unfollowed {self.target.name}')
                        await self.interaction.response.send_message(f'You have unfollowed {self.target.mention}', ephemeral=True)



class NSFW():
    def __init__(self, interaction, user):
        self.interaction = interaction
        self.user = user

    async def mdni(self):
        found = False
        for category in self.interaction.guild.categories:
            if self.user.name in category.name:
                nsfw_category = category
                found = True
        if found:
            await nsfw_category.edit(nsfw=True)
            for channel in nsfw_category.channels:
                await channel.edit(nsfw=True)
            print(f'The environment for {self.user} has been age restricted.')
            await self.interaction.response.send_message(f'The personal channels of {self.user.mention} are now age restricted.', ephemeral=True)


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
        await self.interaction.response.send_message('All caught up!')

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
        await self.interaction.response.send_message('All caught up!')


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
            await new_category.edit(position=1)
            print(f'Category {new_category.name} moved to the top')
        elif new_category:
            await self.message.channel.parent.edit(position=0)
            print(f'Forum {self.message.channel.parent} moved to the top')

    
