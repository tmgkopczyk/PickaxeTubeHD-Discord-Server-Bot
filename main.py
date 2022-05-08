import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import os
from keep_alive import keep_alive
from datetime import datetime
import requests
import json
from pprint import pprint

from discord.ext.tasks import loop

import twitch

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())


welcome_msg_id = 954489003002974208
my_secret = os.environ["TOKEN"]
#hypixel_api_key = os.environ["Hypixel_API_Key"]
pickaxetubehd_teal = 0x2bc7ad



@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command(name='kick', help='Kicks a member from the server.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("Kicked {0} for reason {1} ".format(member.mention, reason)) 

@client.command()
async def announcement(ctx):
    await ctx.message.delete()
    users = twitch.get_users(config["watchlist"])
    streams = twitch.get_streams(users)
    profiles = twitch.get_profile_data(users)
    stream = streams[0]
    game_info = twitch.get_game_info(stream['game_name'])
    game_id = game_info[0]['id']
    game_preview_url = 'https://static-cdn.jtvnw.net/ttv-boxart/{}-600x800.jpg'.format(game_id)
    for user in range(len(profiles)):
      if profiles[user]['display_name'] == stream['user_name']:       
        data = {
          "content": "Hey @everyone, {} is now live over at [https://www.twitch.tv/{}](https://www.twitch.tv/{})!".format(stream['user_name'],stream['user_login'],stream['user_login']),
          "embeds":[{
            "title": stream['title'],
            "description": "{} is now live on Twitch!".format(stream['user_name']),
            "url": "https://twitch.tv/{}".format(stream['user_login']),
            "color": pickaxetubehd_teal,
            "timestamp": "{}".format(datetime.now()),
            "footer": {
              "icon_url": "https://cdn.discordapp.com/avatars/971060069825392691/9303e0604e5fe669844c13862e545368.png",
              "text": "Twitch"
            },
            "thumbnail": {
              "url": game_preview_url
            },
            "image": {
              "url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1280x720.jpg".format(stream['user_login'])
            },
            "author": {
              "name": stream['user_name'],
              "icon_url": profiles[user]['profile_image_url']
            },
            "fields": 
                [
                  {
                    "inline": True, "name": "Playing", "value": stream['game_name']
                  }, 
                  {
                "inline": True, "name": "Viewer Count", "value": stream['viewer_count']
                  }
                ]
                  }
              ]
            }
        url = "https://discord.com/api/webhooks/971060069825392691/_8DBJn28yj6FF2aLh0UDP09nOcDzygNHC0lu-mMf3bVHjzrtaqhGLtjsYAYjRw4SjCJO"
        result = requests.post(url, json=data)

@client.event
async def on_raw_reaction_add(payload):
    msg_id = welcome_msg_id
    if msg_id == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '👍':
            role = discord.utils.get(guild.roles, name="Subscribers")
        await member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    msg_id = welcome_msg_id
    if msg_id == payload.message_id:
        guild = await (client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '👍':
            role = discord.utils.get(guild.roles, name="Subscribers")
        member = await (guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")


@client.command(pass_context=True, hidden=True)
async def bye(ctx):
    welcome_msg = discord.Embed(
        title='Welcome to the official Server of PickaxeTubeHD!',
        description='React to this mesage to gain access to the server!',
        color=pickaxetubehd_teal,
        timestamp=datetime.now())
    msg = await ctx.channel.send(embed=welcome_msg)
    await msg.add_reaction('👍')


@client.command(
    name='ban',
    help='Bans specifc member from the server that the user mentions.')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("Banned {0} for reason {1} ".format(member.mention, reason))


@client.command(name='unban',
                help='Unbans the mentioned user from the server.')
@commands.has_permissions(administrator=True)
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    unban = discord.Embed(
        title="Success!",
        description="{} has been successfully unbanned.".format(user.mention))
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=unban)
        await guild.unban(user=user)


@client.command(
    name='poll',
    help='Allows users to have good discussions about certain topics.')
async def poll(ctx, message, *options):
    indicator_list = ['🇦', '🇧', '🇨', '🇩']
    close_ended_question_responder = ['👍', '👎']
    poll = discord.Embed(
        title=message,
        description="{}".format('\n'.join(options)),
        color=pickaxetubehd_teal,
        timestamp=datetime.now(),
    )
    msg = await ctx.channel.send(embed=poll)
    if len(options) > 1:
        for i in range(len(options)):
            await msg.add_reaction(indicator_list[i])
    elif len(options) == 1:
        for i in range(len(close_ended_question_responder)):
            await msg.add_reaction(close_ended_question_responder[i])


@client.command(name='socials', help='Displays the socials of PickaxeTubeHD.')
async def socials(ctx):
    socials_list = [
        "YouTube", "https://www.youtube.com/channel/UCHMXHaWoFTa4FRsm7aLaUbQ",
        "Twitter", "https://twitter.com/PickaxeTubeHD", "Twitch",
        "https://www.twitch.tv/pickaxetubehd"
    ]
    linktree = discord.Embed(title='Socials',
                             description="\n".join(socials_list),
                             color=pickaxetubehd_teal,
                             timestamp=datetime.now())
    await ctx.channel.send(embed=linktree)


@client.command(name='ping',
                help="Checks the bot's response time to the server.")
async def ping(ctx):
    ping = discord.Embed(
        title='Pong!',
        description="Your ping to the client is {}ms!".format(
            round(client.latency * 1000)),
        color=pickaxetubehd_teal,
        timestamp=datetime.now(),
    )
    await ctx.channel.send(embed=ping)


@client.command(name='lockdown',
                help="locks down the channel that the user names.")
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=False)
    await ctx.send('{} is now in lockdown'.format(ctx.channel.mention))


@client.command(name='unlock',
                help='Unlocks the channel that was previously locked.')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=True)
    await ctx.send('{} has been unlocked'.format(ctx.channel.mention))


@client.command(name='changenick',
                help='Changes the specified user\'s server name.',
                pass_context=True)
async def changenick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send('Nickname was changed for {}'.format(member.mention))


@client.command(name='clear',
                help="clears the number of messages from a channel")
@commands.has_permissions(manage_channels=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@client.command(name='profile',
                help="sends an embed message to the announcements channel.")
async def profile(ctx):
    users = twitch.get_users(config["watchlist"])
    streams = twitch.get_streams(users)
    profiles = twitch.get_profile_data(users)
    for user in range(len(profiles)):
      if profiles[user]['display_name'] =='pickaxetubehd':
        user_info = profiles[user]
        print(user_info)
        streamer_profile = discord.Embed(
          title = '{}'.format(user_info['display_name']),
          url = "https://twitch.tv/{}".format(user_info['login']),
          description = '{}'.format(user_info['description']),
          timestamp = datetime.now(),
          color = pickaxetubehd_teal
        )
        streamer_profile.add_field(name = "View Count",value = '{}'.format(user_info['view_count']))
        streamer_profile.set_image(url = user_info['offline_image_url'])
        streamer_profile.set_author(name = '{}'.format(user_info['display_name']),icon_url="{}".format(user_info["profile_image_url"]))
        streamer_profile.set_footer(text='Twitch', icon_url='https://cdn.discordapp.com/avatars/971060069825392691/9303e0604e5fe669844c13862e545368.png')

@client.command(name='ticket',help = 'Sends a ticket to the developers')
async def ticket(ctx,reason):
  id = ctx.author.display_name
  ticket_entry = {}
  ticket_entry["Username: {}".format(id)] = "Reason: {}".format(reason)
  ticket = json.dumps(ticket_entry)
  with open('ticket_list.json','a') as file:
    file.write("{}\n".format(ticket))
    file.close()
  ticket_submission_msg = discord.Embed(
    title = "Message Received",
    description = "Thank you for submitting a ticket, {}. We appreciate your feedback.".format(ctx.message.author),
    timestamp = datetime.now(),
    color = pickaxetubehd_teal
  )
  await ctx.author.send(embed = ticket_submission_msg)
    
@client.command(name='stream',
                help="sends an embed message to the announcements channel.")
async def stream(ctx):
    await ctx.message.delete()
    users = twitch.get_users(config["watchlist"])
    streams = twitch.get_streams(users)
    profiles = twitch.get_profile_data(users)
    stream = streams[0]
    game_info = twitch.get_game_info(stream['game_name'])
    game_id = game_info[0]['id']
    game_preview_url = 'https://static-cdn.jtvnw.net/ttv-boxart/{}-600x800.jpg'.format(game_id)
    for user in range(len(profiles)):
      if profiles[user]['display_name'] == stream['user_name']:
        twitch_announcement = discord.Embed(
          title = stream['title'],
          url = "https://twitch.tv/{}".format(stream['user_login']),
          description = "{} is now live on Twitch!".format(stream['user_name']),
          timestamp = datetime.now(),
          color = pickaxetubehd_teal
        )
        twitch_announcement.add_field(name = "Playing",value = '{}'.format(stream['game_name']))
        twitch_announcement.add_field(name = "Viewer Count",value = '{}'.format(stream['viewer_count']), inline = True)
        twitch_announcement.set_footer(text='Twitch', icon_url='https://cdn.discordapp.com/avatars/971060069825392691/9303e0604e5fe669844c13862e545368.png')
        twitch_announcement.set_author(name = stream['user_name'],icon_url = profiles[user]['profile_image_url'])
        twitch_announcement.set_image(url = 'https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1280x720.jpg'.format(stream['user_login']))
        twitch_announcement.set_thumbnail(url=game_preview_url)
        await ctx.send(content = "Hey everyone, {} is now live over at https://www.twitch.tv/{}".format(stream['user_name'],stream['user_login']), embed=twitch_announcement)
      elif profiles[user]['display_name'] != stream['user_name']:
        continue

  
with open("config.json") as config_file:
    config = json.load(config_file)

keep_alive()
client.run(my_secret)
