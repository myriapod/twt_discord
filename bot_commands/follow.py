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