import discord
from discord.ext import commands
from bot.historicaldata.scrape import current_season_scrape
from bot.historicaldata.scrape import career_scrape
import pandas as pd

df_cur = current_season_scrape()
excel_path = 'bot/historicaldata/historical_player_data.xlsx'
df_hist = pd.read_excel(excel_path)
current_year = 2023

df_career = career_scrape()

# remove columns for career stats
columns_remove = [
    'GP_RANK',
    'MIN_RANK',
    'FGM_RANK',
    'FGA_RANK',
    'FG_PCT_RANK',
    'FG3M_RANK',
    'FG3A_RANK',
    'FG3_PCT_RANK',
    'FTM_RANK',
    'FTA_RANK',
    'FT_PCT_RANK',
    'OREB_RANK',
    'DREB_RANK',
    'REB_RANK',
    'AST_RANK',
    'STL_RANK',
    'BLK_RANK',
    'TOV_RANK',
    'PF_RANK',
    'PTS_RANK',
    'AST_TOV_RANK',
    'STL_TOV_RANK'
]

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
        
    # top players for specific stat
    @commands.command()
    async def statstop(self, ctx, stat, amt):
        print("Command recieved")
        
        # check paramters
        isInt = True
        try:
            amt = int(amt)
        except ValueError:
            isInt = False
            
        df_length = len(df_career)

        if not isInt:
            await ctx.send(f"Enter an positive integer between 1 and {df_length}")
            return
        
        if amt > df_length or amt < 1:
            await ctx.send(f"Please input a number between 1 and {df_length}")
            return
        
        stat_match = df_career.columns.str.contains(stat.upper())

        if not stat_match.any():
            await ctx.send(f"{stat} is not a metric. See statshelp for the list of statistics.")
            return
        
        stat_rank = stat.upper() + "_RANK"
        print_statement = f"**{stat.upper()}:**\n"
        
        count = 0
        count_sends = 1
        break_loop = False
        for i in range(1, amt+1):
            df_temp = df_career[df_career[stat_rank] == i].reset_index(drop=True)
            
            # if there are multiple players with the same rank
            for j in range(len(df_temp)):
                if count >= amt:
                    break_loop = True
                    break
                
                name=df_temp["PLAYER_NAME"][j]
                val=df_temp[stat.upper()][j]
                print_temp = f"{count+1}: {name}, {val}\n"

                # check if message length is appopriate length
                if len(print_statement) + len(print_temp) > 2000: 
                    await ctx.send(print_statement)
                    print_statement = f"**{stat.upper()}** part {count_sends}\n"
                else:
                    print_statement+=print_temp
                count+=1

            if break_loop:
                break

        await ctx.send(print_statement)

    # player ranking for specific stat
    @commands.command()
    async def statsrank(self, ctx, first_name, last_name, stat):
        print("Command recieved")
        player_full_name = first_name + " " + last_name

        name_match = df_career['PLAYER_NAME'].str.lower() == player_full_name.lower()
        stat_match = df_career.columns.str.contains(stat.upper())

        if not name_match.any():
            await ctx.send(f"{player_full_name} is not in the database!")
            return
        
        if not stat_match.any():
            await ctx.send(f"{stat} is not a metric. See statshelp for the list of statistics.")
            return
    
        df_career_player = df_career[name_match].reset_index(drop=True)

        # column name for ranking
        stat_rank = stat.upper() + "_RANK"

        await ctx.send(f"{stat}: {df_career_player[stat.upper()][0]}\nRank: {df_career_player[stat_rank][0]}\n")

    # players career/total stats
    @commands.command()
    async def statscareer(self, ctx, first_name, last_name): 
        print("Command recieved")
        player_full_name = first_name + " " + last_name

        name_match = df_career['PLAYER_NAME'].str.lower() == player_full_name.lower()

        if not name_match.any():
            await ctx.send(f"{player_full_name} is not in the database!")
            return
        
        df_career_player = df_career[name_match].reset_index(drop=True)
        df_career_player.drop(columns=columns_remove, inplace=True)
        await ctx.send(format_df_print(df_career_player, player_full_name))
        
    # players stats by season
    @commands.command()
    async def statsszn(self, ctx, first_name, last_name, season_type, year):
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


