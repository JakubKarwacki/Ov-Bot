import discord, random, json
from discord.ext import commands

class Bot_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        ### Settings ###
        with open("settings.json") as json_file:
            self.settings = json.load(json_file)

        ### Data ###
        with open("data.json") as json_file:
            self.data = json.load(json_file)
        self.maps = self.data["Maps"]
        self.champions = self.data["Champions"]

        ### Variables ###
        self.participants, self.teams, self.roles = [], {}, ["Damage", "Damage", "Tank", "Support", "Support"]

    ### Local functions ###
    def split_participants(self, ctx, reshuffle=None):
        needed, to_return = self.settings["in_team"]*self.settings["teams"], ""

        #Reshuffle
        if reshuffle:
            if reshuffle == "teams": random.shuffle(self.participants)
            elif reshuffle == "roles": random.shuffle(self.roles)
            elif reshuffle == "both":
                random.shuffle(self.participants)
                random.shuffle(self.roles)

        #Split participants
        in_team = len(self.participants)//self.settings["teams"] if needed > len(self.participants) else self.settings["in_team"]
        for x in range(self.settings["teams"]): self.teams["Team "+str(x+1)] = self.participants[in_team*x:in_team*(x+1):]
        
        #Complete participants
        if needed > len(self.participants) and len(self.participants)%self.settings["teams"]:
            self.teams["Team 1"].append(self.participants[-1])
        elif needed < len(self.participants):
            self.teams["Reserve"] = self.participants[self.settings["in_team"]*self.settings["teams"]::]

        #Teams display
        for key in self.teams.keys():
            to_return += "`"+key+"`\n"
            for id, t in enumerate(self.teams[key]):
                to_return += "*"+str(id+1)+": "+(ctx.guild.get_member(t).nick or ctx.guild.get_member(t).name)+"*\n"
            to_return += "\n"
        return to_return

    @commands.command()
    async def team_up(self, ctx: commands.Context, *args):
        """Form two teams (up to 5 members) and a reserve (available if on in bot settings) based on online server members or actual voice channel members."""
        if args:
            if args[0] in ["here", "h"]:
                voice = self.author.voice
                if voice:
                    self.participants = [x.id for x in voice.channel.members if not x.bot]
                    await ctx.send("**Teams formed from voice channel members!**")
                else:
                    await ctx.send("**Not in a voice channel!**")
            else:
                await ctx.send("**Unknown parameter!**")
        else:
            self.participants = [y.id for y in ctx.guild.members if not y.bot]
            await ctx.send("**Teams formed from server online members!**")
    
    @commands.command()
    async def list(self, ctx: commands.Context):
        """Show list of team up participants."""
        await ctx.send("**Viewing the list of participants!**\n`Participants:`\n"+' '.join(["*"+str(id+1)+": "+(self.guild.get_member(x).nick or self.guild.get_member(x).name)+"*\n" for id, x in enumerate(self.participants)]))

    #Add participant to the list.
    @commands.command()
    async def add(self, ctx: commands.Context, *args):
        """Add participant to the list."""
        for x in args:
            [self.participants.append(y.id) for y in ctx.guild.members if x in (y.nick, y.name) and not x.bot]
        await ctx.send("**Participants added to the list!**")
        self.split_participants(ctx)

    #Remove participant from the list.
    @commands.command()
    async def remove(self, ctx: commands.Context, *args):
        """Remove participant from the list."""
        for x in args:
            [self.participants.pop(y.id) for y in ctx.guild.members if x in (y.nick, y.name)]
        await ctx.send("**Participants removed from the list!**")
        self.split_participants(ctx)

    #Swaps team members with each other.
    @commands.command()
    async def swap(self, ctx: commands.Context, *args):
        """Swaps participants with each other."""
        self.participants[args[0]-1], self.participants[args[1]-1] = self.participants[args[1]-1], self.participants[args[0]-1]
        await ctx.send("**Participants swaped!**")
        self.split_participants(ctx)

    #Shuffle (teams / roles / both).
    @commands.command()
    async def shuffle(self, ctx: commands.Context, reshuffle="teams"):
        """Shuffle (teams / roles / both)."""
        await ctx.send("**Teams reshuffled!**")
        self.split_participants(ctx, reshuffle)

    #Select one from all or those belonging to a specific game mode maps.
    @commands.command()
    async def pick_map(self, ctx: commands.Context, teams=False):
        """Select one from all or those belonging to a specific game mode maps."""
        mode_step = self.maps[random.randint(0,len(self.maps))]
        mode = [x for x in mode_step.keys()][0]
        map = mode_step.get(mode)[random.randint(0,len(mode_step.get(mode)))]
        name = map.get("name")
        src = map.get("src")

        embed = discord.Embed(title=name, description="Mode: *"+mode+"*", color=0xF79D20)
        embed.set_image(url=src)
        if teams:
            embed.add_field(name="Teams", value=self.split_participants(ctx, "teams"), inline=False)
        await ctx.send(embed=embed)

    #Creates a ban vote for all teams for hero bans (one per role) or for a specific team.
    @commands.command()
    async def ban_vote(self, ctx: commands.Context):
        """Creates a ban vote for all teams for hero bans (one per role) or for a specific team."""
        return

    #Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings).
    @commands.command()
    async def next_game(self, ctx: commands.Context):
        """Form two teams, pick a map and ban heroes (one per role for every team* available if on in bot settings)."""
        await self.pick_map(ctx, True)
    
    @commands.command()
    async def new_game(self, ctx: commands.Context):
        await self.team_up(ctx)
        await self.next_game(ctx)
    
    @commands.command()
    async def on_command_error(self, ctx: commands.Context, error): 
        if isinstance(error, commands.CommandNotFound): 
            await ctx.send("Command unknown! Check **ov!help** for more informations!")

def setup(bot: commands.Bot):
    bot.add_cog(Bot_Commands(bot))
