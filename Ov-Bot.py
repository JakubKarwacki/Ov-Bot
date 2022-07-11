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
participants, teams, roles = [], {}, ["Damage", "Damage", "Tank", "Support", "Support"]

### Local functions ###
def split_participants(ctx, reshuffle=None):
    global participants, teams
    needed, to_return = settings["in_team"]*settings["teams"], ""

    #Reshuffle arg
    if reshuffle:
        if reshuffle == "teams": random.shuffle(participants)
        elif reshuffle == "roles": random.shuffle(roles)
        elif reshuffle == "both":
            random.shuffle(participants)
            random.shuffle(roles)

    #Split participants
    in_team = len(participants)//settings["teams"] if needed > len(participants) else settings["in_team"]
    for x in range(settings["teams"]): teams["Team "+str(x+1)] = participants[in_team*x:in_team*(x+1):]
    
    #Complete participants
    if needed > len(participants) and len(participants)%settings["teams"]:
        teams["Team 1"].append(participants[-1])
    elif needed < len(participants):
        teams["Reserve"] = participants[settings["in_team"]*settings["teams"]::]

    #Teams display
    for key in teams.keys():
        to_return += "`"+key+"`\n"
        for t in teams[key]:
            to_return += "*"+(ctx.guild.get_member(t).nick or ctx.guild.get_member(t).name)+"*\n"
        to_return += "\n"
    return to_return

### Ov-Bot commands ###
#Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.
@bot.command(name='team-up', aliases=['t'], help='Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members.')
async def team_up(ctx, *args):
    global participants
    #Get participants
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
    
    #Slice participants into teams
    await ctx.send(split_participants(ctx, True))
    

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
    split_participants(ctx)

#Remove participant from the list.
@bot.command(name='remove', aliases=['r'], help='Remove participant from the list.')
async def remove(ctx, *args):
    for x in args:
        [participants.pop(y.id) for y in ctx.guild.members if x in (y.nick, y.name)]
    await ctx.send("**Participants removed from the list!**")
    split_participants(ctx)

#Swaps team members with each other.
@bot.command(name='swap', aliases=['sw'], help='Swaps participants with each other.')
async def swap(ctx, *args):
    participants[args[0]-1], participants[args[1]-1] = participants[args[1]-1], participants[args[0]-1]
    await ctx.send("**Participants swaped!**")
    split_participants(ctx)

#Shuffle (teams / roles / both).
@bot.command(name='shuffle', aliases=['s'], help='Shuffle (teams / roles / both).')
async def shuffle(ctx, reshuffle="teams"):
    await ctx.send("**Teams reshuffled!**")
    split_participants(ctx, reshuffle)

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
