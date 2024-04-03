import pandas as pd
import discord
from discord.ext import commands
from bot.googlecloudstorage.getfromgcs import get_dataframe
from bot.googlecloudstorage.util import get_list_of_players

class Streamers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        print(get_dataframe("Jayson Tatum"))
        print(get_list_of_players())


async def setup(bot):
    await bot.add_cog(Streamers(bot))