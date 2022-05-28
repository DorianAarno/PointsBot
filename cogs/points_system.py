from disnake import *
from disnake.ext import commands
from assets import functions as func
import traceback
import asyncio
from SpamFilter import AntiSpam
from config import POINTS_TO_BE_GIVEN_PER_MESSAGE

class PointsSystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.author.bot or not msg.guild:
            return
        try:
            if await AntiSpam(dictionary=True).check(self.bot, msg.channel, msg.author):
                return

            datas = await func.DataFetch(self.bot, 'all', 'points', msg.guild.id)
            if len(datas) != 0:
                for data in datas:
                    if data[1] == msg.author.id:
                        AuthorData = data
                        break
                    else:
                        AuthorData = None
                if AuthorData:
                    await func.DataUpdate(self.bot, f"UPDATE points SET points = {AuthorData[2]+POINTS_TO_BE_GIVEN_PER_MESSAGE} WHERE guild_id = {AuthorData[0]} and user_id = {AuthorData[1]}")
                else:
                    await func.DataUpdate(self.bot, f"INSERT INTO points(guild_id, user_id, points) VALUES(?,?,?)", msg.guild.id, msg.author.id, POINTS_TO_BE_GIVEN_PER_MESSAGE)
            else:
                await func.DataUpdate(self.bot, f"INSERT INTO points(guild_id, user_id, points) VALUES(?,?,?)", msg.guild.id, msg.author.id, POINTS_TO_BE_GIVEN_PER_MESSAGE)
        except:
            print(traceback.format_exc())

def setup(bot):
    bot.add_cog(PointsSystem(bot))
