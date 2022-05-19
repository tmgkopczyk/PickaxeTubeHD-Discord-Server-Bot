import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import os
from keep_alive import keep_alive
from datetime import datetime,timezone

import requests
import json
import twitch

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())


welcome_msg_id = 954489003002974208
my_secret = os.environ["TOKEN"]
hypixel_api = os.environ["Hypixel_API_Key"]
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
async def hypixel(ctx, username,gamemode,profile_name=None):
  mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'.format(username)).json()
  uuid = mojangData['id']
  hypixel = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hypixel_api,uuid)).json()
  playerStats = []
  gamemode_list = hypixel['player']['stats']
  playerStats = []
  if profile_name == None:
    for game in gamemode_list:
      if gamemode == game:
        for stat in gamemode_list[game]:
          playerStats.append("{}: {}".format(stat, gamemode_list[game][stat]))
        break
    hypixel_stats = discord.Embed(
      title = "{}'s Stats for {}".format(username,gamemode),
      description = "\n".join(playerStats),
      timestamp = datetime.now(),
      color = pickaxetubehd_teal
    )
    hypixel_stats.set_thumbnail(url='https://crafatar.com/avatars/{}?size=&default=MHF_Steve&overlay'.format(uuid))
    await ctx.send(embed=hypixel_stats)
  else:
    skyblockData = requests.get('https://api.hypixel.net/skyblock/profiles?key={}&uuid={}'.format(hypixel_api,uuid)).json()
    profile_list = skyblockData['profiles']
    playerStats = []
    for profile in range(len(profile_list)):
      if profile_list[profile]['cute_name'] == profile_name:
        member_list = profile_list[profile]['members']
        for member in member_list:
          if member == uuid:
            for stat in member_list[member]['stats']:
              playerStats.append("{}: {}".format(stat, int(member_list[member]['stats'][stat])))
            break
    skyblock_stats = discord.Embed(
      title = "{}'s Stats for {}".format(username,gamemode),
      description = "\n".join(playerStats),
      timestamp = datetime.now(),
      color = pickaxetubehd_teal
    )
    skyblock_stats.set_thumbnail(url='https://crafatar.com/avatars/{}?size=&default=MHF_Steve&overlay'.format(uuid))
    await ctx.send(embed=skyblock_stats)


  
@client.command()
async def video(ctx):
    api_key = "AIzaSyDY9NziRx7HW8Fw6b5JiAmUlan2_LgF1Dg"
    youtube = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id=UCHMXHaWoFTa4FRsm7aLaUbQ&key={}".format(api_key))
    upload_playlist = youtube.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    uploads = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={}&key={}".format(upload_playlist,api_key))
    uploads = uploads.json()['items']
    newest_video = uploads[0]
    video_id = newest_video['contentDetails']['videoId']
    video_info = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(video_id,api_key))
    video_info = video_info.json()
    upload_info = video_info['items'][0]
    video_id = upload_info['id']
    channel_name = upload_info['snippet']['channelTitle']
    video_link = "https://www.youtube.com/watch?v={}".format(video_id)
    print(newest_video)
    data = {
   "content":"Hey @everyone, {} just posted a new video over at {}. Go check it out!".format(channel_name,video_link)
    }
    url = ["https://discord.com/api/webhooks/974284926440595487/UjrP-N3d6OLhx_wGlceciQJv0ia9m3xpXreXpua3gArUs-hSvmpkK2HXsKcmwj6ySiHQ","https://discord.com/api/webhooks/975204350177734656/bCfwTQHfpnWNexoDwS_ak_XlQXNDaqNAtWkuOBf74J4Cm7_Z0uxFhxwOwcXFj3fDF3nU"]
    for link in range(len(url)):
      result = requests.post(url=url[link],json=data)
      
@client.command()
async def stream(ctx):
    await ctx.message.delete()
    utc_now = int(datetime.utcnow().timestamp())
    users = twitch.get_users(config["watchlist"])
    streams = twitch.get_streams(users)
    profiles = twitch.get_profile_data(users)
    for i in range(len(streams)):
      stream = streams[i]
      tags = twitch.get_stream_tags(stream['user_id'])
      game_info = twitch.get_game_info(stream['game_name'])
      game_id = game_info[0]['id']
      tag_list=[]
      game_preview_url = 'https://static-cdn.jtvnw.net/ttv-boxart/{}-600x800.jpg'.format(game_id)
      profiles = twitch.get_profile_data(users)
      utc = datetime.utcnow().timestamp()
      for i in range(len(profiles)):
        profile = profiles[i]
        if profile['display_name'] == stream['user_name']:
          for i in range(len(tags)):
            tag_list.append(tags[i]['localization_names']['en-us'])
          data = {
   "content":"Hey @everyone, {} went live on Twitch!".format(stream['user_name']),
   "embeds":[
      {
        "title":stream['title'],
        "description":"{} is now live on Twitch!".format(stream['user_name']),
        "url":"https://www.twitch.tv/{}".format(stream['user_login']),
        "color":6570404,
        "timestamp":stream['started_at'],
        "footer":{
            "text":"Twitch | {}".format(", ".join(tag_list)),
          "icon_url":"https://cdn.discordapp.com/avatars/971060069825392691/9303e0604e5fe669844c13862e545368.png"
         },
      "thumbnail": {
        "url": game_preview_url
        },
        
         "image":{
            "url":"https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1920x1080.jpg?{}".format(stream['user_login'],int(utc))
         },
         "author":{
            "name":stream['user_name'],
            "icon_url":profile['profile_image_url']
         },
         "fields":[
            {
               "name":"Playing",
               "value":stream['game_name'],
               "inline":True
            },
            {
               "name":"Viewer Count",
               "value":stream['viewer_count'],
               "inline":True
            }
         ]
      }
   ]
}
      url = "https://discord.com/api/webhooks/970806299803648030/wkKuS24axW8kL-WxiEFlSeGnDFP-w03b65OaDC5Zd3gNFq4Ps6GZjyoGt8hJa-uqFRkA"
      result = requests.post(url=url,json=data)

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

  
with open("config.json") as config_file:
    config = json.load(config_file)

keep_alive()
client.run(my_secret)
