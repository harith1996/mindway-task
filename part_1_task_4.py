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
    "net_loss": "sum"
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
            values = []
            for game_type in GAME_TYPES:
                value = row[stat + "_" + game_type]
                if not np.isnan(value):
                    values.append(value)
            if(stat in AGGR_MAP):
                aggr = AGGR_METHODS[AGGR_MAP[stat]](values)
            df.at[index, stat] = aggr
    #remove individual game type columns
    for game_type in GAME_TYPES:
        for stat in STATS:
            df.drop(stat + "_" + game_type, axis=1, inplace=True)
    return df

def get_percent_lost(sum_stakes, net_loss):
    if sum_stakes == 0:
        return None
    return net_loss/sum_stakes

def recalculate_percent_lost(df):
    for index, row in df.iterrows():
        sum_stakes = row["sum_stakes"]
        net_loss = row["net_loss"]
        percent_lost = get_percent_lost(sum_stakes, net_loss)
        df.at[index, "percent_lost"] = percent_lost
    return df

if __name__ == "__main__":
    df = pd.read_csv("Gambling_data.csv", sep=";")
    df = aggregate_across_all_games(df)
    recalculate_percent_lost(df)
    print(df.head())
    df.to_csv("Gambling_data_aggregated.csv", sep=";", index=False)