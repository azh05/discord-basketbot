from historicaldata.gamelog import scrape_gamelog
import matplotlib.pyplot as plt
import pandas as pd

def graphstatsma(first_name, last_name, start_year, end_year, stat, game_count):
    if start_year > end_year: 
        print("Invalid years, start year must be before end year")
        return

    # make full name
    full_name = first_name.lower().capitalize() + " " + last_name.lower().capitalize()

    # get data from start_year to end_year
    df_gamelog = scrape_gamelog(first_name=first_name, last_name=last_name, year=start_year+1)

    # check empty df
    if df_gamelog is None: 
        print("Empty season")
        start_year += 1
    
    for year in range(start_year+1, end_year):
        df_gamelog_temp = scrape_gamelog(first_name=first_name, last_name=last_name, year=year)

        if df_gamelog is None and not df_gamelog_temp is None:
            df_gamelog = df_gamelog_temp
        
        elif not df_gamelog is None and not df_gamelog_temp is None:
            df_gamelog = pd.concat([df_gamelog, df_gamelog_temp], ignore_index=True).reset_index(drop=True)

    
    sma = df_gamelog[stat].rolling(window=game_count).mean()
    
    long_period = df_gamelog.shape[0]/2.5 if df_gamelog.shape[0] > 20 else df_gamelog.shape[0]/2 # shape gets the number of games in the df
    sma_long = df_gamelog[stat].rolling(window=int(long_period)).mean()

    plt.plot(df_gamelog[stat], label=stat)
    plt.plot(sma, label=f'{game_count}-game SMA')
    plt.plot(sma_long, label='SMA long')

    plt.title(f"{full_name} {stat} for the {int(start_year)}-{end_year%100} season(s)")
    plt.legend()
    plt.xlabel("Game #")
    plt.ylabel(stat)

    plt.show()

if __name__ == '__main__':
    graphstatsma("Jayson", "Tatum", 2023, 2024, "pts", 5)