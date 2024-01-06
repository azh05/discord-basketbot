import discord
from discord.ext import commands

class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        print("Command received")
        await ctx.send("Hi!")

    @commands.command()
    async def hi(self, ctx):
        print("Command received")
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(Greeting(bot))


