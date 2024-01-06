# Basketbot - an NBA Analytics Discord Bot

## Overview
Basketbot is an NBA Analytics Discord Bot that scrapes data from the nba.com website. Currently, it contains basic player stats from the regular season and the playoffs, starting from the 2000-01 regular season. Users can retrieve stats for an individual player, using commands in a discord chat. Commands use the prefix *. In the future, deeper analytics and graphs will be implemented as well as team statistics like Offensive Rating and Defense Rating.

The bot is coded in python and uses discord.py, pandas, requests, and numpy. As the bot is updated, the matplotlib and seaborn libraries are likely to be added. 

## Commands
**Test Greetings:**
    hi - Basketbot says "Hello!"
    hello - Basketbot says "Hi!"

**Player Statistics:**
    statsSzn [first_name] [last_name] [season_type='Regular' or 'Playoffs'] [year] - Basketbot returns Player's stats for specified season