# Basketbot - an NBA Analytics Discord Bot

## Overview
Basketbot is an NBA Analytics Discord Bot that scrapes data from the nba.com website. Currently, it contains basic player stats from the regular season and the playoffs, starting from the 2000-01 regular season. Users can retrieve stats for an individual player, using commands in a discord chat. Commands use the prefix *. In the future, deeper analytics and graphs will be implemented as well as team statistics like Offensive Rating and Defense Rating.

The bot is coded in python and uses discord.py, pandas, requests, numpy, scikit-learn, and matplotlib.

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
* graphplayerstat [first_name] [last_name] [stat] [season_type='Regular' or 'Playoffs'] - graphs the NBA player's stat by year