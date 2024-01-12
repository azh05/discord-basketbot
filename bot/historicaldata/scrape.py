# Scraping Tutorial from Alex Sington
# https://www.youtube.com/watch?v=nHtlRlWmTV4

# for nba API
import requests

# data analysis
import pandas as pd
import numpy as np

# web scraping 
url_2324 = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS"
r = requests.get(url=url_2324).json()
table_headers = r['resultSet']['headers']

# adding season type and year to the data frame
df_cols = ['Year', 'Season_Type'] + table_headers

# request header dictionary
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "macOS",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# current year dataframe (live updates when called)
def current_season_scrape():
    r = requests.get(url=url_2324).json()
    df_cur=pd.DataFrame(columns=df_cols)

    # Regular season
    temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
    temp_df2 = pd.DataFrame({'Year': ['2023-24' for i in range(len(temp_df1))],
                            'Season_Type': ['Regular%20Season' for i in range(len(temp_df1))]})
    
    if not temp_df1.empty and not temp_df2.empty:
        temp_df1 = pd.concat([temp_df2, temp_df1], axis=1)
    
    
    # playoffs
    url_2324_playoffs = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Playoffs&StatCategory=PTS"
    r_playoffs = requests.get(url=url_2324_playoffs).json()
    temp_df3 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
    temp_df4 = pd.DataFrame({'Year': ['2023-24' for i in range(len(temp_df3))],
                            'Season_Type': ['Playoffs' for j in range(len(temp_df3))]})
    
    if not temp_df3.empty and not temp_df4.empty:
        temp_df3 = pd.concat([temp_df4, temp_df3], axis=1)

    df_cur = pd.concat([df_cur, temp_df1], axis=0)
    df_cur = pd.concat([df_cur, temp_df2], axis=0)

    # Data cleaning
    df_cur.drop(columns=['RANK', 'TEAM_ID', 'PLAYER_ID'], inplace=True)
    df_cur['Season_Type'].replace('Regular%20Season', 'Regular', inplace=True)
    df_cur['Year'] = df_cur['Year'].str[:4].astype(int)

    # drop nans
    df_cur = df_cur.dropna()
    return(df_cur)

# create dataframe of stats from years 2000-2023
def historical_scrape():
    df = pd.DataFrame(columns=df_cols)
    season_types = ['Regular%20Season', 'Playoffs']
    years = ['1980-81','1981-82','1982-83','1983-84','1984-85', '1985-86','1986-87','1987-88', '1988-89', '1989-90',
            '1990-91','1991-92','1992-93','1993-94','1994-95', '1995-96','1996-97','1997-98', '1998-99', '1999-00',
            '2000-01','2001-02','2002-03','2003-04','2004-05','2005-06','2006-07','2007-08','2008-09', '2009-10',
            '2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19', '2019-20',
            '2020-21','2021-22','2022-23']

    for y in years:
        for s in season_types:
            api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
            
            r=requests.get(url=api_url, headers=headers).json()
            temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
            temp_df2 = pd.DataFrame({'Year': [y for i in range(len(temp_df1))],
                            'Season_Type': [s for i in range(len(temp_df1))]})
            if not temp_df1.empty and not temp_df2.empty:
                temp_df3 = pd.concat([temp_df2, temp_df1], axis = 1)
                df = pd.concat([df, temp_df3], axis=0)
    
    # Data cleaning
    df.drop(columns=['RANK', 'TEAM_ID', 'PLAYER_ID'], inplace=True)
    df['Season_Type'].replace('Regular%20Season', 'Regular', inplace=True)
    df['Year'] = df['Year'].str[:4].astype(int)

    # store in excel sheet
    path = 'bot/historicaldata/historical_player_data.xlsx'
    df.to_excel(path, index=False)


floattoint = [
    'MIN',
    'FG3M',
    'FG3A',
    'OREB',
    'DREB',
    'REB',
    'STL',
    'BLK',
    'TOV'
]

# scrape career stats
def career_scrape():
    url_career = "https://stats.nba.com/stats/leagueLeaders?ActiveFlag=No&LeagueID=00&PerMode=Totals&Scope=S&Season=All%20Time&SeasonType=Regular%20Season&StatCategory=PTS"
    r=requests.get(url=url_career, headers=headers).json()
    df_career = pd.DataFrame(r['resultSet']['rowSet'], columns=r['resultSet']['headers'])
    df_career.drop(columns=['PLAYER_ID'], inplace=True)

    df_career[floattoint] = df_career[floattoint].fillna(0).astype('int64')

    return(df_career)
    
#career_scrape()
historical_scrape()