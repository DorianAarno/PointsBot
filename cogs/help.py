from disnake import *
from disnake.ext import commands
from assets import functions as func
import traceback
from cogs.points_commands import PointsCommands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self,ctx):
        e = Embed(title=":notepad_spiral: Help Menu :notepad_spiral:", description="• Prefix is .\n•View more about each command using `.help <command-name>`, for Example: `.help points`", color=ctx.author.color)
        e.add_field(name="Commands", value="• `points`\n• `name`\n• `add`\n• `remove`\n• `leaderboard`\n• `shop`")
        await ctx.send(embed=e)

    @help.command(name='points')
    async def spoints(self,ctx):
        e = Embed(title=":coin: Points", description=f"View how many {PointsName} you or someone has.", color=ctx.author.color)
        e.add_field(name="Syntax", value="`.points` or `/points display`")
        await ctx.send(embed=e)

    @help.command()
    async def name(self,ctx):
        e = Embed(title=":coin: Points Name", description=f"Rename {PointsName}.", color=ctx.author.color)
        e.add_field(name="Syntax", value="`.points name <name>` or `/points name <name>`")
        await ctx.send(embed=e)

    @help.command()
    async def add(self,ctx):
        e = Embed(title=":coin: Points Add", description=f"Supply {PointsName} to any member.", color=ctx.author.color)
        e.add_field(name="Syntax", value="`.points add <member> <number>` or `/points add <member> <number>`")
        await ctx.send(embed=e)

    @help.command()
    async def remove(self,ctx):
        e = Embed(title=":coin: Points Remove", description=f"Remove {PointsName} from any member.", color=ctx.author.color)
        e.add_field(name="Syntax", value="`.points remove <member> <number>` or `/points remove <member> <number>`")
        await ctx.send(embed=e)

    @help.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        e = Embed(title=":arrow_double_up: Leaderboard", description="See ranking of all members.", color=ctx.author.color)
        e.add_field(name="Syntax", value="`.lb` or `/leaderboard`")
        await ctx.send(embed=e)

    @help.command()
    async def shop(self, ctx):
        e = Embed(title=":shopping_cart: Shop", description=f"A MarketPlace for utilizing {PointsName}.", color=ctx.author.color)
        e.add_field(name="Commands", value="`.shop`: Shows the shop\n`.shop add <price> <item-name>`: Add a item in the shop.\n`.shop remove`: Remove a item from the shop.\n`.shop buy`: Buy a item from the shop.")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Help(bot))
