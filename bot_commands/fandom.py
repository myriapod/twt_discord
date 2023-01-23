import discord


class Fandom():
    def __init__(self, reaction):
        self.member = reaction.member
        self.guild = self.member.guild
        self.msg_id = reaction.message_id

    async def assign_fandom(self, reaction_channel):
        message = await reaction_channel.fetch_message(self.msg_id)
        fandom_name = message.content

        fandom_role = discord.utils.get(
            self.guild.roles, name=fandom_name)

        await self.member.add_roles(fandom_role)  # type: ignore
        print(f"[REACT ROLE] added role {fandom_role.name} to user {self.member.name}")