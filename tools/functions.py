import tools.permissions as permissions


async def create_env(member):
    """
    Creates the environment for member, made of:
    - role [member.name] assigned to the member
    - role [member.name-follower]
    - category [member.name-mega-zone]
    - forum channel [member.name-feed]
    - text channel [member.name-zone]
    - voice channel [member.name-space]
    """
    # create the name role
    role = await member.guild.create_role(name=member.name)

    # create the name-follow role
    followers = await member.guild.create_role(name=f'{member.name}-follower')

    # assign their name role
    await member.add_roles(role)

    # permissions for category, forum and voice
    overwrites = {
        member.guild.default_role: permissions.default_no_read,
        member.guild.get_role(role.id): permissions.channel_owner,
        member.guild.get_role(followers.id): permissions.tl_follower
    }
    overwrites_text = {
        member.guild.default_role: permissions.default_no_read,
        member.guild.get_role(role.id): permissions.channel_owner,
        member.guild.get_role(followers.id): permissions.text_follower
    }

    # create personal channels and categories
    category = await member.guild.create_category(f'{member.name}-mega-zone', overwrites=overwrites)

    text_channel = await member.guild.create_text_channel(name=f'{member.name}-zone', category=category, overwrites=overwrites_text)

    forum_channel = await member.guild.create_forum(name=f'{member.name}-feed', category=category, overwrites=overwrites)

    voice_channel = await member.guild.create_voice_channel(name=f'{member.name}-space', category=category, overwrites=overwrites)

    print(f'The environment for {member.name} is set up.')


async def manual_env(ctx, member):
    """
    Command to manually set up the environment if needed
    Implies that the name role and the follower role have been manually created
    Useful for when the bot gets rate limited on creating roles
    """
    role = None
    followers = None
    for grole in ctx.guild.roles:
        if member.name == grole.name:
            role = grole
        elif member.name+"-follower" == grole.name:
            followers = grole

    if role and followers:
        await create_env(member)
    else:
        print(f"ERROR: Roles for {member.name} weren't manually set up")
        # await ctx.channel.send(f"ERROR: Roles for {member.mention} weren't manually set up")


def get_member_roles(member):
    """
    NOT USED function:
    get the roles of the user-linked roles from the user
    """
    roles = []
    for role in member.guild.roles:
        if role.name == member.display_name:
            roles.append(role)
        elif role.name == f'{member.display_name}-follower':
            roles.append(role)
    return roles


async def follow(interaction, member, user):
    """
    Function to follow a user as member
    // Could be rewritten better
    """
    r_name = f'{user.name}-follower'

    # values to make the bot verbose
    already_following = False
    user_found = False

    for role in interaction.guild.roles:
        if role.name == r_name:
            user_found = True

            # check to see if the member isn't already following the requested user
            for m_role in member.roles:
                if role == m_role:
                    print(f'{member.name} is already following {user.name}')
                    await interaction.response.send_message(f'{member.name} is already following {user.name}')
                    already_following = True

            if not already_following:
                await member.add_roles(role)
                print(f'{member.name} is now following {user.name}')
                await interaction.response.send_message(f'{member.mention} is now following {user.mention}')

    if not user_found:
        print(f'The user {user.name} is not in the server.')
        await interaction.response.send_message(f"Couldn't find {user.name} in the server.")


def find_category(interaction, name):
    categories = interaction.guild.categories
    for cat in categories:
        if cat.name == name:
            return cat


def find_channel(guild, name):
    for cat in guild.channels:
        if cat.name == name:
            return cat
