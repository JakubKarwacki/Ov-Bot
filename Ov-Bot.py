import discord, random, json, math
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='ov!', intents=intents, help_command=commands.MinimalHelpCommand(no_category = 'Commands'))

### Token ###
with open("tokens.json") as json_file:
    tokens = json.load(json_file)

### Settings ###
with open("settings.json") as json_file:
    settings = json.load(json_file)

### Data ###
with open("data.json") as json_file:
    data = json.load(json_file)

### Variables ###
participants, teams, display = [], {}, ""


### Local functions ###
def teams_display(ctx):
    global participants, teams, display
    indicator = ""
    for id, x in enumerate(participants):
        if id == 0:
            indicator = "Team 1"
            display += "`"+indicator+":`\n"
        elif not id%(len(participants)//settings["teams"]) and id//(len(participants)//settings["teams"]) <= settings["teams"]:
            indicator = "Team "+str(id%((len(participants)-len(participants)%settings["teams"])//settings["teams"])+2)
            display += "\n`"+indicator+":`\n"
        elif id%(len(participants)//settings["teams"]) and id//(len(participants)//settings["teams"]) == settings["teams"]:
            indicator = "Reserve"
            display += "`"+indicator+":`\n"
        display += "*"+str(id%(len(participants)//settings["teams"])+1)+": "+str(ctx.guild.get_member(x).nick or ctx.guild.get_member(x).name)+"*\n"
    
    return display

### Ov-Bot commands ###
#Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.
@bot.command(name='team-up', aliases=['t'], help='Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.')
async def team_up(ctx, *args):
    global participants
    if args:
        if args[0] in ["here", "h"]:
            voice = ctx.author.voice
            if voice:
                participants = [x.id for x in voice.channel.members if not x.bot]
                await ctx.send("**Teams formed from voice channel members!**")
            else:
                await ctx.send("**Not in a voice channel!**")
        else:
            await ctx.send("**Unknown parameter!**")
    else:
        participants = [y.id for y in ctx.guild.members if not y.bot]
        await ctx.send("**Teams formed from server online members!**")

    random.shuffle(participants)
    await ctx.send(teams_display(ctx))

#Show list of team up participants.
@bot.command(name='list', aliases=['l'], help='Show list of team up participants.')
async def list(ctx):
    global participants
    await ctx.send("**Viewing the list of participants!**\n`Participants:`\n"+' '.join(["*"+str(id+1)+": "+(ctx.guild.get_member(x).nick or ctx.guild.get_member(x).name)+"*\n" for id, x in enumerate(participants)]))

#Add participant to the list.
@bot.command(name='add', aliases=['a'], help='Add participant to the list.')
async def add(ctx, *args):
    for x in args:
        [participants.append(y.id) for y in ctx.guild.members if x in (y.nick, y.name) and not x.bot]
    await ctx.send("**Participants added to the list!**")
    await ctx.send(teams_display(ctx))

#Remove participant from the list.
@bot.command(name='remove', aliases=['r'], help='Remove participant from the list.')
async def remove(ctx, *args):
    for x in args:
        [participants.pop(y.id) for y in ctx.guild.members if x in (y.nick, y.name)]
    await ctx.send("**Participants removed from the list!**")
    await ctx.send(teams_display(ctx))

#Swaps team members with each other.
@bot.command(name='swap', aliases=['sw'], help='Swaps participants with each other.')
async def swap(ctx, *args):
    participant_wait = args[0]
    participants[args[0]-1] = participants[args[1]-1]
    participants[args[1]-1] = participants[participant_wait]
    await ctx.send("**Participants swaped!**")
    await ctx.send(teams_display(ctx))

#Shuffle (teams / roles / both).
@bot.command(name='shuffle', aliases=['s'], help='Shuffle (teams / roles / both).')
async def shuffle(ctx):
    random.shuffle(participants)
    await ctx.send("**Teams reshuffled!**")
    await ctx.send(teams_display(ctx))

#Select one from all or those belonging to a specific game mode maps.
@bot.command(name='pick-map', aliases=['p'], help='Select one from all or those belonging to a specific game mode maps.')
async def pick_map(ctx):
    return

#Creates a ban vote for all teams for hero bans (one per role) or for a specific team.
@bot.command(name='ban-vote', aliases=['b'], help='Creates a ban vote for all teams for hero bans (one per role) or for a specific team.')
async def ban_vote(ctx):
    return

#Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings).
@bot.command(name='custom-game', aliases=['c'], help='Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings).')
async def pick_game(ctx):
    return


@bot.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        await ctx.send("Command unknown! Check **ov!help** for more informations!")

bot.run(tokens["token"])
