import discord
from discord.ext import commands

token = ""


def get_role_id(member):
    """
    Useful function:
    get the id of the user-linked role from the user
    Improvement possible: could be getting the role itself, not useful for now
    """
    for role in member.guild.roles:
        if role.name == member.display_name:
            return role.id


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    """
    Set up the environment for the new user when they join
    """
    print(f'{member.name} has joined the server!')
    # create the name role
    role = await member.guild.create_role(name=member.display_name)

    # create the name-follow role
    followers = await member.guild.create_role(name=f'{member.display_name}-follower')

    # assign their name role
    await member.add_roles(role)

    # create personal channels and categories
    # permissions for category, forum and voice
    overwrites = {
        member.guild.default_role: discord.PermissionOverwrite(read_messages=False),

        member.guild.get_role(role.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=True,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=True,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=True,
            external_emojis=True,
            use_external_emojis=True,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=True,
            manage_permissions=False,
            manage_webhooks=True,
            manage_emojis=True,
            manage_emojis_and_stickers=True,
            use_application_commands=True,
            request_to_speak=True,
            manage_events=True,
            manage_threads=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=True),

        member.guild.get_role(followers.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=False,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=False,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=False,
            send_tts_messages=False,
            manage_messages=False,
            embed_links=False,
            attach_files=False,
            read_message_history=True,
            mention_everyone=False,
            external_emojis=False,
            use_external_emojis=False,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=False,
            manage_permissions=False,
            manage_webhooks=False,
            manage_emojis=False,
            manage_emojis_and_stickers=False,
            use_application_commands=False,
            request_to_speak=False,
            manage_events=False,
            manage_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=False)
    }
    # special permissions for the text channel to allow followers to talk more freely
    overwrites_text = {
        member.guild.default_role: discord.PermissionOverwrite(read_messages=False),

        member.guild.get_role(role.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=True,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=True,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=True,
            external_emojis=True,
            use_external_emojis=True,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=True,
            manage_permissions=False,
            manage_webhooks=True,
            manage_emojis=True,
            manage_emojis_and_stickers=True,
            use_application_commands=True,
            request_to_speak=True,
            manage_events=True,
            manage_threads=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=True),

        member.guild.get_role(followers.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=False,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=False,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=False,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=False,
            external_emojis=False,
            use_external_emojis=False,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=False,
            manage_permissions=False,
            manage_webhooks=False,
            manage_emojis=False,
            manage_emojis_and_stickers=False,
            use_application_commands=True,
            request_to_speak=False,
            manage_events=False,
            manage_threads=False,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=False)
    }

    category = await member.guild.create_category(f'{member.display_name}-mega-zone', overwrites=overwrites)

    text_channel = await member.guild.create_text_channel(name=f'{member.display_name}-zone', category=category, overwrites=overwrites_text)

    forum_channel = await member.guild.create_forum(name=f'{member.display_name}-tl', category=category, overwrites=overwrites)

    voice_channel = await member.guild.create_voice_channel(name=f'{member.display_name}-space', category=category, overwrites=overwrites)

    print(f'The environment for {member.name} is set up.')


@bot.event
async def on_member_remove(member):
    """
    When a user leaves, their channels and roles get deleted
    Some of it should be optional for optimisation
    """
    print(f'{member.name} has left.')

    role_id = get_role_id(member)
    role = member.guild.get_role(role_id)
    await role.delete()

    # for the test phase mostly - delete channels
    channel_list = member.guild.by_category()
    for channel in channel_list:
        category = channel[0]
        if category and member.display_name in category.name:
            await category.delete()
            for chan in channel[1]:
                await chan.delete()

    print(f'The environment for {member.name} has been removed.')


@bot.command(name="follow")
async def follow(ctx, user):
    """
    Bot command to call with !follow
    Assigns the role name-follower to the user requesting
    """
    member = ctx.message.author
    r_name = f'{user}-follower'

    for mem in ctx.guild.members:
        if mem.display_name == user:
            followee = mem

    for role in ctx.guild.roles:
        if role.name == r_name:
            await member.add_roles(role)
            print(f'{member.name} is now following {user}')
            await ctx.channel.send(f'{member.mention} is now following {followee.mention}')


@bot.command(name="create")
async def create_set_up(ctx):
    """
    Command to manually set up the environment if needed
    definitely shouldnt be just repeated code from on_member_join lmao
    """
    member = ctx.message.author
    role = await member.guild.create_role(name=member.display_name)
    followers = await member.guild.create_role(name=f'{member.display_name}-follower')
    await member.add_roles(role)
    overwrites = {
        member.guild.default_role: discord.PermissionOverwrite(read_messages=False),

        member.guild.get_role(role.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=True,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=True,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=True,
            external_emojis=True,
            use_external_emojis=True,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=True,
            manage_permissions=False,
            manage_webhooks=True,
            manage_emojis=True,
            manage_emojis_and_stickers=True,
            use_application_commands=True,
            request_to_speak=True,
            manage_events=True,
            manage_threads=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=True),

        member.guild.get_role(followers.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=False,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=False,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=False,
            send_tts_messages=False,
            manage_messages=False,
            embed_links=False,
            attach_files=False,
            read_message_history=True,
            mention_everyone=False,
            external_emojis=False,
            use_external_emojis=False,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=False,
            manage_permissions=False,
            manage_webhooks=False,
            manage_emojis=False,
            manage_emojis_and_stickers=False,
            use_application_commands=False,
            request_to_speak=False,
            manage_events=False,
            manage_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=False)
    }
    overwrites_text = {
        member.guild.default_role: discord.PermissionOverwrite(read_messages=False),

        member.guild.get_role(role.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=True,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=True,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=True,
            external_emojis=True,
            use_external_emojis=True,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=True,
            manage_permissions=False,
            manage_webhooks=True,
            manage_emojis=True,
            manage_emojis_and_stickers=True,
            use_application_commands=True,
            request_to_speak=True,
            manage_events=True,
            manage_threads=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=True),

        member.guild.get_role(followers.id): discord.PermissionOverwrite(
            create_instant_invite=True,
            kick_members=False,
            ban_members=False,
            administrator=False,
            manage_channels=False,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            priority_speaker=False,
            stream=True,
            read_messages=True,
            view_channel=True,
            send_messages=True,
            send_tts_messages=True,
            manage_messages=False,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            mention_everyone=False,
            external_emojis=False,
            use_external_emojis=False,
            view_guild_insights=False,
            connect=True,
            speak=True,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=False,
            manage_permissions=False,
            manage_webhooks=False,
            manage_emojis=False,
            manage_emojis_and_stickers=False,
            use_application_commands=True,
            request_to_speak=False,
            manage_events=False,
            manage_threads=False,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            external_stickers=True,
            use_external_stickers=True,
            use_embedded_activities=True,
            moderate_members=False)
    }
    category = await member.guild.create_category(f'{member.display_name}-mega-zone', overwrites=overwrites)
    text_channel = await member.guild.create_text_channel(name=f'{member.display_name}-zone', category=category, overwrites=overwrites_text)
    forum_channel = await member.guild.create_forum(name=f'{member.display_name}-tl', category=category, overwrites=overwrites)
    voice_channel = await member.guild.create_voice_channel(name=f'{member.display_name}-space', category=category, overwrites=overwrites)

bot.run(token)
