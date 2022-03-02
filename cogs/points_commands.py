from disnake import *
from disnake.ext import commands
from assets import functions as func
import traceback
from config import PointsName
from Paginator import CreatePaginator

class PointsCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def points(self,ctx,member:Member = None):
        member = member or ctx.author
        data = await func.DataFetch(self.bot, 'one', 'points', ctx.guild.id, member.id)
        if data:
            points = data[2]
        else:
            points = 0
        e = Embed(title=f"{member.name}'s {PointsName}", description=f":coin: {points} {PointsName}", color=Color.gold())
        try:
            e.set_thumbnail(url=member.avatar.url)
        except:
            pass
        await ctx.send(embed=e)

    async def edit(self, ctx, member, number):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'You are not allowed to use this command.'))
        data = await func.DataFetch(self.bot, 'one', 'points', ctx.guild.id, member.id)
        EditedPoints = data[2]+number
        if EditedPoints < 0:
            EditedPoints = 0
        if data:
            await func.DataUpdate(self.bot, f"UPDATE points SET points = {EditedPoints} WHERE guild_id = {ctx.guild.id} and user_id = {member.id}")
        else:
            await func.DataUpdate(self.bot, f"INSERT INTO points(guild_id, user_id, points) VALUES(?,?,?)", ctx.guild.id, member.id, EditedPoints)
        if number > 0:
            method = 'increased'
        else:
            method = 'decreased'
        await ctx.send(embed=func.SuccessEmbed(f'{PointsName} Edited!', f"{member.name}'s :coin: {PointsName} was {method} by `{number}`."))

    @points.command()
    async def remove(self, ctx, member:Member, number:int):
        if number <= 0:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'Number needs to be greater than 0.'))
        await self.edit(ctx, member, -number)

    @remove.error
    async def remove_error(self,ctx,error):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.send(embed=func.ErrorEmbed('Error', 'Correct syntax is: `.points remove <member> <number>`. Use slash command for more simplicity.'))

    @points.command()
    async def add(self, ctx, member: Member, number: int):
        if number <= 0:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'Number needs to be greater than 0.'))
        await self.edit(ctx, member, number)

    @add.error
    async def add_error(self,ctx,error):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.send(embed=func.ErrorEmbed('Error', 'Correct syntax is: `.points add <member> <number>`. Use slash command for more simplicity.'))

    @commands.command(aliases=['lb'])
    async def leaderboard(self,ctx):
        datas = await func.DataFetch(self.bot, 'all', 'points', ctx.guild.id)
        datas = sorted(datas, key=lambda x: x[2], reverse=True)
        embeds = [Embed(title=f":arrow_double_up: {PointsName} Leaderboard :arrow_double_up:", color=Color.gold())]
        vals = 0
        CurrentEmbed = 0
        UserData = None
        UserRank = None
        for i, data in enumerate(datas):
            if data[1] == ctx.author.id:
                UserRank = i+1
                UserData = data
            if vals <= 9:
                embeds[CurrentEmbed].add_field(name=f"# {i+1}", value=f"<@{data[1]}> [:coin: {data[2]}]", inline=False)
                vals += 1
            else:
                embeds.append(Embed(color=Color.gold()))
                CurrentEmbed += 1
                vals = 0
                embeds[CurrentEmbed].add_field(name=f"# {i+1}", value=f"<@{data[1]}> [:coin: {data[2]}]", inline=False)

        for embed in embeds:
            if UserData:
                embed.set_footer(text=f'# {UserRank} {ctx.author.name} [🪙 {data[2]}]', icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except:
                pass
        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
        else:
            await ctx.send(embed=embeds[0], view=CreatePaginator(embeds, ctx.author.id))

def setup(bot):
    bot.add_cog(PointsCommands(bot))
