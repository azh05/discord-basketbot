# Basketbot - an NBA Analytics Discord Bot

## Overview
Basketbot is an NBA Analytics Discord Bot that scrapes data from the nba.com and basketball-reference.com websites. Currently, it contains basic player stats from the regular season and the playoffs, starting from the 1980-81 regular season. Game logs for players can be retrieved from any season for any player on basketball-reference. Users can retrieve stats for an individual player, using commands in a discord chat. Commands use the prefix *. In the future, deeper analytics and graphs will be implemented as well as team statistics like Offensive Rating and Defense Rating.

The bot is coded in python and uses discord.py, pandas, requests, BeautifulSoupm, numpy, scikit-learn, and matplotlib.

## Setup 
Create a discord bot using the instructions on https://discord.com/developers/docs/getting-started. Clone the repository. Create a .env file and save your discord bot token as DISCORD_BOT_TOKEN. Run pip install .

## Commands
**Greetings:**
* hi - Basketbot says "Hello!"
* hello - Basketbot says "Hi!"

**Player Statistics:**
* statsszn [first_name] [last_name] [season_type='Regular' or 'Playoffs'] [year] - prints NBA player's stats for specified season to chat
* statsrank [first_name] [last_name] [stat] - prints NBA player's ranking on the all time leaderboard for a stat
* statstop [stat] [amt] - prints the top 'amt' players in a particular stat by career stats
* statscareer [first_name] [last_name] - prints NBA player's career/total stats

**Graph Player Statistics:**
* graphstatbyyear [first_name] [last_name] [stat] [season_type='Regular' or 'Playoffs'] - graphs the NBA player's stat by year
* graphstatbygame [first_name] [last_name] [stat] [year] - graphs the NBA player's stat by game for a particular year