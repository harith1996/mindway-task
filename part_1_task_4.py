#build data points across multiple game types
import pandas as pd
import numpy as np

GAME_TYPES = ["fixedodds", "liveaction", "casino"]
STATS = ["duration", "sum_stakes", "sum_bets", "bettingdays", "frequency", "bets_per_day", "euros_per_bet", "net_loss", "percent_lost"]

AGGR_MAP = {
    "sum_stakes": "sum",
    "sum_bets": "sum",
    "bettingdays": "sum",
    "duration": "sum",
    "frequency": "mean",
    "bets_per_day": "mean",
    "euros_per_bet": "mean",
    "net_loss": "sum",
    "percent_lost": "mean"
}

AGGR_METHODS ={
    "sum": np.sum,
    "mean": np.mean
}

#aggregation strategies
# for all sum stats, use sum
# for net loss, use sum
# for betting days, use sum
# for duration, use sum
# for per day stats, use mean
# for percent lost, use mean
# for frequency, use mean
# for euros per bet, use mean

def aggregate_across_all_games(df):
    #iterate over all rows in df
    for index, row in df.iterrows():
        for stat in STATS:
            aggr = 0
            for game_type in GAME_TYPES:
                value = row[stat + "_" + game_type]
                if not np.isnan(value):
                    aggr += value
            df.at[index, stat] = aggr
    return df

if __name__ == "__main__":
    df = pd.read_csv("Gambling_data.csv", sep=";")
    df = aggregate_across_all_games(df)
    print(df.head())