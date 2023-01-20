def rules(guild, bot_channel, role_assignment, general_category, general_text, general_voice, kpop_channel):
    return f'''
Welcome to the {guild.name} server!

This is the server map that will help guide you through the server. (Items below listed by order of appearance in the server channel list.)

**[1] Bot commands**
{bot_channel.mention} is where you can use the bot and its / commands. Use the `/help` command to display the list of commands available.

**[2] Reaction roles**
{role_assignment.mention} is a channel where you can assign yourself fandom roles. They are purely for cosmetic purposes and don't bring special access to any of the fandom forums as they are accessible to everyone on the server by default. A new role is created when a forum for a fandom is created.

**[3] General chats**
**{general_category.mention}** is the general text ({general_text.mention}) and voice chat ({general_voice.mention}) that everyone in the server has access to.

**[4] Fandom sub-spaces**
**{kpop_channel.mention}** is a semi-organized place that everyone can access. There are forums dedicated to certain bands/topics that users can create using the bot command `/forum`.

**[5] Personal sub-spaces**
The rest of the server is **personal categories** that can be accessed by others through the `/follow` command.

Each member gets a [your discord username]-MEGA-ZONE category that regroups:
- [your discord username]-FEED forum channel: only you can create new forum posts, but your followers (the people who have access to your personal category) can respond to them in the threads.
- [your discord username]-SPACE voice channel: you and your followers can join, but you should still have more moderation rights in your own personal voice channel.

You get moderation rights in your own category. You can also change the name of your categories if you want to. (FYI if you do that, it will not automatically remove your categories if you leave the server).
        '''