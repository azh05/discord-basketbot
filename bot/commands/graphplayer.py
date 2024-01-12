import discord
from discord.ext import commands
from bot.historicaldata.scrape import current_season_scrape
from bot.historicaldata.scrape import career_scrape
from bot.historicaldata.gamelog import scrape_gamelog

# for graphing
import pandas as pd
import matplotlib.pyplot as plt
import numpy
from sklearn.linear_model import LinearRegression

# for removing the graph file
import os

df_cur = current_season_scrape()
excel_path = 'bot/historicaldata/historical_player_data.xlsx'
df_hist = pd.read_excel(excel_path)
df_career = career_scrape()
df_combined = pd.concat([df_hist, df_cur], ignore_index=True)

class GraphPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def graphstatbygame(self, ctx, first_name, last_name, stat, year):
        # adjust year to be the same as nba.com year system
        year+=1 
        
        # scrape
        df_gamelog = scrape_gamelog(first_name, last_name, year)

        # check if valid inputss
        if df_gamelog.empty:
            await ctx.send("Invalid name or year!")
            return

        stat_match = df_gamelog.columns.str.contains(stat.lower())

        if not stat_match.any():
            await ctx.send(f"{stat} is not a metric.")
            return
        
        # for graph name
        player_full_name = first_name.lower().capitalize() + " " + last_name.lower().capitalize()

        # create graph
        fig = plt.figure()
        plt.plot(df_gamelog['game_season'], df_gamelog[stat.lower()], marker='o', color='black')
        plt.title(f'{player_full_name}: {year} {stat.upper()} distribution')

        plt.xlabel('Game number')
        plt.ylabel(stat.lower())

        # set appropriate ticks
        min_game = int(df_gamelog['game_season'].min())
        max_game = int(df_gamelog['game_season'].max())

        tick_size = 1
        if max_game - min_game > 60:
            tick_size = 5
        elif max_game - min_game > 40: 
            tick_size = 4
        elif max_game - min_game > 15:
            tick_size = 2
        
        all_years = range(min_game, max_game + 1, tick_size)
        plt.xticks(all_years)

        plt.savefig('plot.png')
        file = discord.File("plot.png")
        
        await ctx.send(file=file)
        os.remove('plot.png')

    @commands.command()
    async def graphstatbyyear(self, ctx, first_name, last_name, stat, season_type):
        print("Command recieved")

        player_full_name = first_name.lower().capitalize() + " " + last_name.lower().capitalize()

        name_match = df_combined['PLAYER'].str.lower() == player_full_name.lower()
        stat_match = df_combined.columns.str.contains(stat.upper())
        season_match = df_combined['Season_Type'].str.lower() == season_type.lower()

        if not name_match.any():
            await ctx.send(f"{player_full_name} is not in the database!")
            return
        
        if not stat_match.any():
            await ctx.send(f"{stat} is not a metric. See statshelp for the list of statistics.")
            return
        
        # change for season_type contents for better print
        if season_type.lower() == "regular":
            season_type = "Regular Season" 
        
        df_player = df_combined[name_match & season_match].reset_index(drop=True)

        # creating plot
        fig = plt.figure()
        plt.plot(df_player['Year'], df_player[stat.upper()], marker='o', linestyle='-', color='black')
        plt.title(f'{player_full_name}: Career {stat.upper()} distribution for the {season_type}')
        plt.xlabel('Year')
        plt.ylabel(stat.upper())

        # range of years for graph
        min_year = int(df_player['Year'].min())
        max_year = int(df_player['Year'].max())
        all_years = range(min_year, max_year + 1, 2)

        # creating linear regression line - line of best fit
        X = df_player[['Year']]
        y = df_player[stat.upper()]
        model = LinearRegression()
        model.fit(X, y)

        plt.plot(df_player['Year'], model.predict(X), color='blue', linestyle='--', label='Line of Best Fit')

        plt.xticks(all_years)
        plt.savefig('plot.png')
        file = discord.File("plot.png")
        
        await ctx.send(file=file)
        os.remove('plot.png')
        
async def setup(bot):
    await bot.add_cog(GraphPlayer(bot))