import discord, os
from discord.ext import commands
from dotenv import load_dotenv

def main():
    load_dotenv()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='ov!', intents=intents, help_command=None)
    bot.load_extension("cog")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command! Check **ov!help** for more informations!")

    bot.run(os.getenv('api_key'))

main()