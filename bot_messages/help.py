def help(role_assignment):
    return f'''
List of available commands:
- `/help` : displays this message
- `/follow [user to follow]` : grants you access to the personal channels of the person you want to follow
- `/unfollow [person to unfollow]` : removes the access to the personal channels of the person you want to unfollow
- `/mdni` : puts an age restriction on your personal channels
- `/fandom [name] [emoji] [hex color]` : creates a dedicated forum (accessible to everyone) and colored role that you can assign yourself in the {role_assignment.mention} channel
        '''