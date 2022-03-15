import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
import os
import threading
import requests
import json
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup






intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix = ">", intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=">help | v1.2.1"))
    print("Trak Bot is operational.")



# @client.command()
# async def datadump(ctx,pass_context=True):
#   await ctx.send("**ALPHA VERSION\nA VERY LONG LIST WILL OCCUR**")
#   id = ctx.message.guild.id
#   print(id)
#   # initial setup
#   URL = "https://data.vatsim.net/v3/vatsim-data.json"

#   # json entries
#   response = urllib.request.urlopen(URL)
#   str_response = response.read().decode('utf-8')
#   obj = json.loads(str_response)


#   # result is connections
#   # print(obj["general"]["connected_clients"])

#   for pilot in obj['pilots']:
#     await ctx.send((pilot["callsign"],pilot['latitude'],pilot['longitude']))
#     # (pilot['latitude'],pilot['longitude'])


@client.command()
async def stats(ctx):
   # initial setup
  URL = "https://data.vatsim.net/v3/vatsim-data.json"

  # json entries
  response = urllib.request.urlopen(URL)
  str_response = response.read().decode('utf-8')
  obj = json.loads(str_response)

  clients = (obj["general"]["connected_clients"])
  version = (obj["general"]["version"])
  embed=discord.Embed(title=f"VATSIM Statistics", color = discord.Color.green())
  embed.add_field(name = "Connected Clients", value = f"{clients}")
  embed.add_field(name = "Version (Velocity)", value = f"{version}")
  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/831007172388323348/947666205530021898/projecttrak.png")
  embed.set_footer(text=f"© Project Trak | © Spherical Systems 2022")
  await ctx.send(embed=embed)

# @client.command()
# async def onlinecontrollers(ctx):
#   URL = "https://api.vatsim.net/api/facilities/"

  
  
#   response = urllib.request.urlopen(URL)
#   str_response = response.read().decode('utf-8')
#   obj = json.loads(str_response)

#   await ctx.send("**A long list may appear, use wisely.**")

  
#   for s in range(len(obj)):
# 	  if obj[s]["callsign"]:
# 		  await ctx.send("{}".format(obj[s]["callsign"]))
  
@client.command()
async def metar(ctx, *, icao: str):
  # https://api.flybywiresim.com/metar/KLAX?source=vatsim
  URL = f"https://api.flybywiresim.com/metar/{icao}?source=vatsim"

  # json entries
  response = urllib.request.urlopen(URL)
  str_response = response.read().decode('utf-8')
  obj = json.loads(str_response)

  icao = (obj["icao"])
  raw_metar = (obj["metar"])
  embed=discord.Embed(title=f"{icao}",color = discord.Color.green())
  embed.add_field(name = "METAR", value = f"{raw_metar}")
  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/831007172388323348/947666205530021898/projecttrak.png")
  embed.set_footer(text=f"© Project Trak | © Spherical Systems 2022")
  await ctx.send(embed=embed)
  print(icao)


@client.command()
async def simbrief(ctx, *, username: str):

  # We fetch the API url
  URL = f"https://www.simbrief.com/api/xml.fetcher.php?username={username}&json=1"

  # We parse it
  response = urllib.request.urlopen(URL)
  str_response = response.read().decode('utf-8')
  obj = json.loads(str_response)

  # techincal
  user_id = (obj["api_params"]["pid"])
  airac = (obj["params"]["airac"])

  # flight information
  airline_icao = (obj["api_params"]["airline"])
  flight_num = (obj["api_params"]["fltnum"])
  route = (obj["api_params"]["route"])
  origin = (obj["api_params"]["orig"])
  dest = (obj["api_params"]["dest"])
  alt = (obj["api_params"]["altn"])
  name = (obj["api_params"]["cpt"])
  aircraft_type = (obj["api_params"]["type"])
  altitude = (obj["general"]["initial_altitude"])

  # weather
  origin_weather = (obj["weather"]["orig_metar"])
  dest_weather = (obj["weather"]["dest_metar"])

  # pdf installation
  directory = (obj["files"]["directory"])
  link = (obj["files"]["pdf"]["link"])
  file = (f"{directory}{link}")

  
  
  embed=discord.Embed(title=f"OFP for {name} | {airline_icao}{flight_num} | {aircraft_type}", color = discord.Color.green())
  embed.add_field(name = "Departure", value = f"{origin}")
  embed.add_field(name = "Arrival", value = f"{dest}")
  embed.add_field(name = "Alternate", value = f"{alt}")
  embed.add_field(name = "Filed Altitude", value = f"{altitude}", inline = False)
  embed.add_field(name = "Route", value = f"{route}", inline = False)
  embed.add_field(name = f"{origin} METAR", value = f"{origin_weather}", inline = False)
  embed.add_field(name = f"{dest} METAR", value = f"{dest_weather}\n\n[Download OFP PDF File]({file})", inline = False)
  embed.set_footer(text=f"© Project Trak | © Spherical Systems 2022 | AIRAC {airac} | User: {user_id}")
  await ctx.send(embed=embed)
  


@client.command()
async def controller(ctx,cid: str):
  # https://api.vatsim.net/api/ratings/1465400/

  response = urllib.request.urlopen(f"https://api.vatsim.net/api/ratings/{cid}")
  data = json.load(response)
  rating = data['rating']
  region = data['region']
  division = data['division']

  embed=discord.Embed(title=f"Information for {cid}", color = discord.Color.green())
  embed.add_field(name = "Region", value = f"{region}")
  embed.add_field(name = "Rating", value = f"{rating}", inline = False)
  embed.add_field(name = "Divison", value = f"{division}")
  embed.set_footer(text=f"© Project Trak | © Spherical Systems 2022")
  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/831007172388323348/947666205530021898/projecttrak.png")
  await ctx.send(embed=embed)

  


                    


@client.command()
async def help(ctx):
  embed=discord.Embed(title=f"Welcome to the help menu.", color = discord.Color.green())
  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/831007172388323348/947666205530021898/projecttrak.png")
  embed.add_field(name = ">simbrief [username]", value = f"Receive flight information filed on Simbrief.", inline = False)
  embed.add_field(name = ">metar [icao]", value = f"Receive weather information for specified ICAO.", inline = False)
  embed.add_field(name = ">stats", value = f"Receive information on connected clients on VATSIM right now.", inline = False)
  embed.add_field(name = ">controller [cid]", value = f"Receive information on specified controller. *This version does not provide for full information.*", inline = False)
  embed.set_footer(text=f"© Project Trak | © Spherical Systems 2022")
  await ctx.send(embed=embed)

@client.command()
async def github(ctx):
  embed=discord.Embed(title=f"Interested in contribution?", color = discord.Color.green())
  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/831007172388323348/947666205530021898/projecttrak.png")
  embed.add_field(name = "GitHub", value = f"Project Trak is an open source organization dedicated to providing VATSIM resources, and tracking software.\n\n[GitHub Organization](https://github.com/trakvatsim)", inline = False)
  await ctx.send(embed=embed)

client.run(os.getenv("TOKEN"))

