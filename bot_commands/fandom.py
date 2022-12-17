import discord


class Fandom():
    def __init__(self, reaction):
        self.member = reaction.member
        self.guild = self.member.guild
        self.msg_id = reaction.message_id

    async def assign_fandom(self, reaction_channel):
        message = await reaction_channel.fetch_message(self.msg_id)
        self.fandom_name = message.content

        self.fandom_role = discord.utils.get(
            self.guild.roles, name=self.fandom_name)

        await self.member.add_roles(self.fandom_role)  # type: ignore
