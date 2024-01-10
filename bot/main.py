import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
import os

# load bot token key
load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# list of cog files
cog_files = ["commands.hello", "commands.getplayer", "commands.graphplayer"]

# set intents
intents = Intents.all()
bot = commands.Bot(command_prefix="*", intents=intents)

# signify bot runnning
@bot.event
async def on_ready():
    print("Bot is ready for use")
    print("--------------------")
    print("List of commands:")
    await load_commands()
    for command in bot.commands:
        print(command.name)
    

# load commands
async def load_commands():
    for cog_file in cog_files:
        try:
            await bot.load_extension(cog_file)
            print(f"{cog_file} loaded")
        except Exception as e:
            print(f"Failed to load {cog_file}: {e}")

# run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)