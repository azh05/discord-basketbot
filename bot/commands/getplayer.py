import discord
from discord.ext import commands
from bot.historicaldata.scrape import current_season_scrape
import pandas as pd

df_cur = current_season_scrape()
excel_path = 'bot/historicaldata/historical_player_data.xlsx'
df_hist = pd.read_excel(excel_path)
current_year = 2023

# format player stats df for printing to discord chat
def format_df_print(df, player_name):
    if df.empty:
        return(f"Player missing from database! {player_name} may not have played enough games")

    stats_string=""

    # iterate through each instance of player in df
    for i in range(len(df)):
        # iterate through each column
        for column_name in df.columns:
            stats_string += f"{column_name}: {str(df[column_name][i])}\n"
    return(stats_string)

# cog to get player stats by season or career
class GetPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def statsSzn(self, ctx, first_name, last_name, season_type, year):
        print("Command received")

        # checking parameters
        if season_type.lower() != "regular" and season_type.lower() != "playoffs":
            await ctx.send("Season type must be either 'Regular' or 'Playoffs'")
            return
        
        isInt = True
        try:
            year = int(year)
        except ValueError:
            isInt = False
            
        if(not isInt or (year < 2000 or year > 2023)):
            await ctx.send("Year must be an integer between 2000 and 2023")
            return
        
        player_full_name = first_name + " " + last_name

        if int(year) == current_year:
            name_match = df_cur['PLAYER'].str.lower() == player_full_name.lower()
            season_match = df_cur['Season_Type'].str.lower() == season_type.lower()

            df_player_row = df_cur[name_match & season_match].reset_index(drop=True)

            await ctx.send(format_df_print(df_player_row, player_full_name))
            return
        
        else:
            name_match = df_hist['PLAYER'].str.lower() == player_full_name.lower()
            season_match = df_hist['Season_Type'].str.lower() == season_type.lower()
            year_match = df_hist['Year'] == year
            
            df_player_row = df_hist[name_match & year_match & season_match].reset_index(drop=True)

            await ctx.send(format_df_print(df_player_row, player_full_name))
            return
        
async def setup(bot):
    await bot.add_cog(GetPlayer(bot))


