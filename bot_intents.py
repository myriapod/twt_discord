import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True
intents.guilds = True
intents.webhooks = True