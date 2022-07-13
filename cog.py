import discord, random, json
from discord.ext import commands

class Game_Management(commands.Cog):
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
                to_return += f"*{id+1}: <@!{t}>*\n"
            to_return += "\n"
        return to_return
    
    async def move(self, ctx):
        vc = [x for x in ctx.guild.voice_channels if x.name in self.settings["channels"]]
        for k_id, key in enumerate(self.teams.keys()):
            for t in self.teams[key]:
                await ctx.guild.get_member(t).move_to(vc[k_id],reason="Teaming up") if ctx.guild.get_member(t).voice else await ctx.send(f"<@!{t}> not connected to the voice chat!")

    #Create teams based on members who are currently online or present on the channel
    @commands.command()
    async def team_up(self, ctx: commands.Context, display=True, *args):
        """Currently online / present on the channel into participants"""
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

    #Participants list
    @commands.command()
    async def list(self, ctx: commands.Context):
        """Participants list"""
        await ctx.send(("**Viewing the list of participants!**\n`Participants:`\n"+' '.join([f"*{id+1}: <@!{x}>*\n" for id, x in enumerate(self.participants)])) if self.participants else "**No participants to display!**")

    #Add participant
    @commands.command()
    async def add(self, ctx: commands.Context, *args):
        """Add participant by their name"""
        before = len(self.participants)
        for x in args:
            [self.participants.append(y.id) for y in ctx.guild.members if x in (y.nick, y.name) and not y.bot]
        if before < len(self.participants):
            await ctx.send("**Participants added to the list!**")
        else:
            await ctx.send("**No such participant/s!**")
        self.split_participants(ctx)

    #Remove participant
    @commands.command()
    async def remove(self, ctx: commands.Context, *args):
        """Remove participants by their name"""
        before = len(self.participants)
        for x in args:
            [self.participants.remove(y.id) for y in ctx.guild.members if x in (y.nick, y.name)]
        if before > len(self.participants):
            await ctx.send("**Participants removed from the list!**")
        else:
            await ctx.send("**No such participant/s!**")
        self.split_participants(ctx)

    #Swap participants
    @commands.command()
    async def swap(self, ctx: commands.Context, *args):
        """Swap participants by their list position"""
        if len(args) != 2:
            await ctx.send("Wrong syntax! Check **ov!help** for more informations!")
        elif not len(self.participants):
            await ctx.send("**No participants to swap!**")
        else:
            self.participants[int(args[0])-1], self.participants[int(args[1])-1] = self.participants[int(args[1])-1], self.participants[int(args[0])-1]
            await ctx.send("**Participant/s swaped!**")

    #Shuffle (teams / roles / both)
    @commands.command()
    async def shuffle(self, ctx: commands.Context, reshuffle="teams"):
        """Shuffle (teams / roles / both)"""
        await ctx.send("**Teams reshuffled!**")
        self.split_participants(ctx, reshuffle)

    #Pick random map
    @commands.command()
    async def pick_map(self, ctx: commands.Context, teams=False, reshuffle=None):
        """Pick random map"""
        mode_step = self.maps[random.randint(0,len(self.maps)-1)]
        mode = [x for x in mode_step.keys()][0]
        map = mode_step.get(mode)[random.randint(0,len(mode_step.get(mode))-1)]
        name = map.get("name")
        src = map.get("src")

        embed = discord.Embed(title=mode+': '+name, color=0xF79D20)
        if teams:
            embed.add_field(name="\u200B", value=self.split_participants(ctx, reshuffle), inline=False)
        embed.set_image(url=src)
        await ctx.send(embed=embed)

    #Vote for hero bans
    '''
    @commands.command()
    async def ban_vote(self, ctx: commands.Context):
        """Vote for hero bans"""
        return
    '''

    #Same team, new map
    @commands.command()
    async def next_game(self, ctx: commands.Context, move=None):
        """Same team new map"""
        await self.pick_map(ctx, True)
        if move in ("move", "m"):
            await self.move(ctx)
    
    @commands.command()
    async def new_game(self, ctx: commands.Context, move=None):
        """Everything you need to start custom game"""
        await self.team_up(ctx)
        await self.pick_map(ctx, True, "teams")
        if move in ("move", "m"):
            await self.move(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(Game_Management(bot))
