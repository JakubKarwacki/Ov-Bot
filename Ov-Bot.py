import discord, os
from discord.ext import commands
from dotenv import load_dotenv

def main():
    load_dotenv()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='ov!', intents=intents)
    bot.load_extension("cog")
    bot.run(os.getenv('api_key'))

main()