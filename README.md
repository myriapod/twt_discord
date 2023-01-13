# twt_discord
A Discord bot to emulate Twitter (sort of) (probably mostly KPOP stan Twitter).

The idea in a few bullet points:
- Create personal private channels for every member of the server that people can "follow" by attributing them a role that grants them access to the channel. The rights and permissions for personal channels are different for their owners and their followers.
- Use restricted forum posts to immitate Twitter posts and a personal feed. The followers can respond to the forum posts but cannot post themselves on someone else's feed.
- Implement a "latest message" feature that brings the channel or category with the most recent activity to the top of the category list.
- Create forums about particular topics that everyone in the server has access to.


# Set up
## Setting up the bot locally
1. Clone the GitHub repo (for now it only works with local hosting) (<a href="https://www.youtube.com/watch?v=zahvzwzdM4Y">guide to run a bot on replit</a> (not personally tested yet))
2. Create a bot in the <a href="https://discord.com/developers/applications">Discord Developer Portal</a> (<a href="https://discordpy.readthedocs.io/en/stable/discord.html">guide</a>)
3. The easiest way to get the bot to work is to give it Administrator permissions. You can use this link to add it to your server by replacing CLIENT_ID with your actual client ID: <&permissions=8&scope=bot>https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot</code>
4. Fill in your token in the .env file
5. Run <code>main.py</code> to make the bot online


## Using the bot to set up the entire server
1. Create a new Community Discord server. **It HAS to be a community server.** (<a href="https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server">guide</a>)
2. Use the <code>/server</code> command to automatically set up channels and categories. Do not modify anything of the server before launching the command or it might not work properly.


# Commands supported
## Accessible to all users
To use a command, type <code>/</code> in any channel (there is a <code>#bot-commands</code> channel created by default) to display the commands menu.
- **help**
- **follow [person to follow]** *(the name inpupt lets you search through the members of the server)* -- grants you access to the personal channels of the person you want to follow
- **unfollow [person to unfollow]** *(the name inpupt lets you search through the members of the server)* -- removes the access to the personal channels of the person you want to unfollow
- **mdni** -- puts an age restriction on your personal channels
- **fandom [name] [emoji] [hex color]** -- creates a dedicated forum (accessible to everyone) and colored role that you can assign yourself in the <code>#reaction-roles</code> channel

## Restricted to the moderation
(in theory not really in execution...)
- **server** -- sets up the server
- **catchup [auto or manual]** -- sets up the personal environment of newcommers who came while the bot was offline (auto: everything is handled by the bot, manual: the personal roles were created manually)
- **make_follow [follower] [followee]** -- force a user (follower) to follow another (followee)

# Planned Improvements & Known Issues
- Get the bot to work in DMs
- Permission-lock some commands
- It gets kind of crowded at the start of the server if people come in a huge wave
- Ways to host the bot and make it available to others easily