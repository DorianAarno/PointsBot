from disnake import *
from disnake.ext.commands import *
from Paginator import CreatePaginator
import traceback
from assets import functions as func
from config import PointsName, Log_channel

class Shop(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LOG_CHANNEL = Log_channel
        # Channel where all purchases are logged.

    @Cog.listener()
    async def on_ready(self):
        import sqlite3
        db = sqlite3.connect('assets/data.sqlite')
        cursor = db.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS shop(guild_id INTEGER, role_id INTEGER, item_name TEXT, description TEXT, price INTEGER, item_number INTEGER, msg TEXT)"
        )

    @group(invoke_without_command=True, case_insensitive=True)
    async def shop(self, ctx):
        datas = await func.DataFetch(self.bot, 'all', 'shop', ctx.guild.id)
        if len(datas) == 0:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'There are no items in shop yet.'))
        embed = Embed(title=f"{PointsName} MarketPlace :shopping_cart:", color=Color.gold(), description="Buy any item using `.shop buy <item-name/item-number>`. Example: `.shop buy 1`")
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except:
            pass
        embeds = [embed]
        current_embed = 0
        vals = 1
        for i, data in enumerate(datas):
            try:
                if data[1] != 123:
                    role = f"\n**Obtainable Role: {ctx.guild.get_role(data[1]).mention}**"
                else:
                    raise()
            except:
                role = ""
            if vals <= 5:
                embeds[current_embed].add_field(name=f"{i+1}     {data[2]}", value=f'> {data[3]}\n**Price: {data[4]} :coin:**'+role, inline=False)
                vals += 1
            else:
                e = Embed(color=Color.gold())
                try:
                    e.set_thumbnail(url=ctx.guild.icon.url)
                except:
                    pass
                e.add_field(name=data[2], value=data[3]+f'\n**Price: {data[4]} :coin:**'+role, inline=False)
                embeds.append(e)
                current_embed += 1
                vals = 1
        if len(embeds) != 1:
            await ctx.send(embed=embeds[0], view=CreatePaginator(embeds, ctx.author.id))
        else:
            await ctx.send(embed=embeds[0])

    async def ShopAdd(self, ctx, item, price, description, role, command):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'You are not allowed to use this command.'))
        if command == 'prefix':
            await ctx.send("Now input a description for the item.")
            msg = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=60.0)
            description = msg.content
            await ctx.send("Now input the name or id of the role you want to give. You can also mention the role. Type `None` to skip (`None` is case sensitive).")
            msg = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=60.0)
            if msg.content != "None":
                try:
                    role = await RoleConverter().convert(ctx, msg.content)
                    if role != None:
                        role = role.id
                    else:
                        raise()
                except:
                    return await ctx.send(embed=func.ErrorEmbed('Error', 'Role not found.'))
                msg = "None"
            else:
                role = 123
                await ctx.send('Now input the message you want to DM the user on purchasing this item.')
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=180.0)
                msg = msg.content
        datas = await func.DataFetch(self.bot, 'all', 'shop', ctx.guild.id)
        for data in datas:
            if data[2].lower() == item.lower():
                return await ctx.send(embed=func.ErrorEmbed('Error', f'There is already a item named {item}. Input a different name next time.'))
        await func.DataUpdate(self.bot, f"INSERT INTO shop(guild_id, role_id, item_name, description, price, item_number, msg) VALUES(?,?,?,?,?,?,?)", ctx.guild.id, role, item, description, price, len(datas)+1, msg)
        await ctx.send(embed=func.SuccessEmbed('Item Added!', f'{item} was added in the shop successfully.'))

    @shop.command()
    async def add(self, ctx, price: int, *, item):
        await self.ShopAdd(ctx, item, price, "", 123, 'prefix')

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, (BadArgument, MissingRequiredArgument)):
            await ctx.send(embed=func.ErrorEmbed('Syntax Error', f'Correct syntax is: `.shop add <price> <item-name>`. Example: `.shop add 20 Sneaker Role`.'))

    @shop.command()
    async def remove(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'You are not allowed to use this command.'))
        datas = await func.DataFetch(self.bot, 'all', 'shop', ctx.guild.id)
        if len(datas) == 0:
            return await ctx.send(embed=func.ErrorEmbed('Error', 'There are no items in shop yet.'))
        items = [x[2] for x in datas]
        embed = Embed(title="Available Items", description='\n'.join([f"{i+1}. {x}" for i, x in enumerate(items)]))
        await ctx.send(content="Input the serial number of the item you wish to remove.", embed=embed)
        msg = await self.bot.wait_for('message', check=lambda m: m.channel.id == ctx.channel.id and m.author.id == ctx.author.id, timeout=120.0)
        try:
            await func.DataUpdate(self.bot, f"DELETE FROM shop WHERE guild_id = {ctx.guild.id} and item_number = {msg.content}")
            for i, data in enumerate(datas):
                await func.DataUpdate(self.bot, f"UPDATE shop SET item_number = ? WHERE guild_id = {ctx.guild.id} and item_number = {data[5]}", i+1)
            await ctx.send(embed=func.SuccessEmbed('Item Removed!', f'Item removed successfully.'))
        except:
            await ctx.send(embed=func.ErrorEmbed('Error', 'Could not remove the item. Make sure the serial number is correct.'))

    async def BuyItem(self, ctx, data, points):
        remaining_points = points - data[4]
        if remaining_points < 0:
            return await ctx.reply(f"You do not have enough {PointsName} :coin: to purchase this item.")
        else:
            pass
            if data[1] != 123:
                await self.bot.wait_until_ready()
                role = ctx.guild.get_role(data[1])
                try:
                    if role != None:
                        rolegained = role.mention
                        if role in ctx.author.roles:
                            return await ctx.send(embed=func.ErrorEmbed('Item already purchased!', 'You already have this item.'))
                        await ctx.author.add_roles(role)
                    else:
                        raise()
                except:
                    rolegained = f"I was unable to give the role."
                    await ctx.reply("I could not give you the role. Please contact staff.")
            else:
                rolegained = "None"
                await ctx.author.send(data[6])
            log_channel = self.bot.get_channel(self.LOG_CHANNEL)
            await func.DataUpdate(self.bot, f"UPDATE points SET points = ? WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}", remaining_points)
            msg = await ctx.reply(embed=func.SuccessEmbed('Item bought!', f'You have bought {data[2]} successfully!'))
            e = Embed(title="New Purchase", description=f"**Item Bought:** {data[2]}\n**Price:** {data[4]} :coin:\n**Role Gained**: {rolegained}", color=Color.green(), timestamp=msg.created_at)
            try:
                e.set_author(icon_url=ctx.author.avatar.url, name=f"{ctx.author} (Click Here)", url=msg.jump_url)
            except:
                e.set_author(name=f"{ctx.author} (Click Here)", url=msg.jump_url)
            await log_channel.send(embed=e)


    @shop.command()
    async def buy(self, ctx, *, item):
        try:
            item = int(item)
            Type = 'num'
        except:
            Type = 'str'
        datas = await func.DataFetch(self.bot, 'all', 'shop', ctx.guild.id)
        points = await func.DataFetch(self.bot, 'one', 'points', ctx.guild.id, ctx.author.id)
        if points:
            points = points[2]
        else:
            points = 0
        length = 0
        for data in datas:
            if Type == 'str':
                if item.lower() == data[2].lower():
                    await self.BuyItem(ctx, data, points)
                else:
                    length += 1
            else:
                if item == data[5]:
                    await self.BuyItem(ctx, data, points)
                else:
                    length += 1
        if length == len(datas):
            return await ctx.send(embed=func.ErrorEmbed('Item not found.', 'I could not find any item with that name or number.'))

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument)):
            await ctx.send(embed=func.ErrorEmbed('Syntax Error', f'Correct syntax is: `.shop buy <item-name/item-number>`. Example: `.shop buy Sneaker Role` or `.shop buy 1`.'))

def setup(bot):
    bot.add_cog(Shop(bot))
