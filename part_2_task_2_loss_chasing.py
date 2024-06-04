import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
import scipy.stats as stats



df = pd.read_csv('Gambling_data.csv', sep=";")

#loss chasing = after losing, player comes back again to get even
#dataset only has aggregated data, so we can't directly tell if a player is chasing losses
#But, if a player P is chasing losses, both bettingdays and percent_lost should be high for P
#approach: assume loss_chasing is proportional to bettingdays * percent_loss
#cons: even better is if we had loss_per_bet

GAME_TYPES = ['fixedodds', 'liveaction', 'casino']
#iterate over all rows in df
for index, row in df.iterrows():
    loss_chase = 0
    for game_type in GAME_TYPES:
        betting_days = row['bettingdays_' + game_type]
        percent_loss = row['percent_lost_' + game_type]
        #check if value is not NaN
        if not np.isnan(betting_days and not percent_loss):
            loss_chase += betting_days * percent_loss       #why add? 
    df.at[index, 'loss_chase'] = loss_chase
    
#print the player with the highest loss_chase
print(df.loc[df['loss_chase'].idxmax()])