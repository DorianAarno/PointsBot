from disnake import *
from disnake.ext import commands
import sqlite3
import traceback

db = sqlite3.connect('assets/data.sqlite')
cursor = db.cursor()

async def DataFetch(bot, command, table, *vals):
    try:
        # There is no use for bot parameter in Sqlite3 but on migration to cloud database like postgresql, you will need it.
        query = f"SELECT * FROM {table}"
        if len(vals) == 1:
            query += f' WHERE guild_id = {vals[0]}'
        elif len(vals) == 2:
            query += f' WHERE guild_id = {vals[0]} and user_id = {vals[1]}'
        else:
            pass
        cursor.execute(query)
        if command == 'all':
            return cursor.fetchall()
        else:
            return cursor.fetchone()
    except:
        print(traceback.format_exc())

async def DataUpdate(bot, query, *vals):
    if len(vals) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, vals)
    db.commit()

def SuccessEmbed(title, description):
    return Embed(title=":ballot_box_with_check: "+title, description=description, color=Color.green())
def ErrorEmbed(title, description):
    return Embed(title=":x: "+title, description=description, color=Color.from_rgb(255,0,0))
