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
