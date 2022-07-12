import json, discord
from discord.ext import commands

### Token ###
with open("tokens.json") as json_file:
    tokens = json.load(json_file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='ov!', intents=intents)
bot.load_extension("cog")
bot.run(tokens["token"])
