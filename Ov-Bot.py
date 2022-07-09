import discord, random
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='ov!', intents=intents, help_command=commands.MinimalHelpCommand(no_category = 'Commands'))

### Settings ###
reserve = 0

### Variables ###
with open('token.txt') as f: token = f.readline()
participants = []

#local functions
def shuffle_local(mode):
    return

### Ov-Bot commands ###
#Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.
@bot.command(name='team-up', aliases=['tu'], help='Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.')
async def team_up(ctx, *args):
    global participants

    if args in ('here', 'h'):
        participants = list(ctx.author.voice.hannel.members)
    else:
        participants =  list(discord.guild.members)
    
    return

#Show list of team up participants.
@bot.command(name='list', aliases=['l'], help='Show list of team up participants.')
async def list():
    return

#Add participant to the list.
@bot.command(name='add', aliases=['a'], help='Add participant to the list.')
async def add():
    return

#Remove participant from the list.
@bot.command(name='remove', aliases=['r'], help='Remove participant from the list.')
async def remove():
    return

#Swaps team members with each other.
@bot.command(name='swap', aliases=['sw'], help='Swaps team members with each other.')
async def swap():
    return

#Shuffle (teams / roles / both).
@bot.command(name='shuffle', aliases=['s'], help='Shuffle (teams / roles / both).')
async def shuffle():
    return

#Select one from all or those belonging to a specific game mode maps.
@bot.command(name='pick-map', aliases=['pm'], help='Select one from all or those belonging to a specific game mode maps.')
async def pick_map():
    return

#Creates a ban vote for all teams for hero bans (one per role) or for a specific team.
@bot.command(name='ban-vote', aliases=['bn'], help='Creates a ban vote for all teams for hero bans (one per role) or for a specific team.')
async def ban_vote():
    return

#Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings).
@bot.command(name='pick-game', aliases=['pg'], help='Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings).')
async def pick_game():
    return

bot.run(token)