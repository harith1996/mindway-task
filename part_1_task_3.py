import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
import scipy.stats as stats



df = pd.read_csv('Gambling_data.csv', sep=";")

GAME_TYPES = ['fixedodds', 'liveaction', 'casino']
COLUMN_PREFIX = 'duration'
rg_cases = {}
control_cases = {}
for game_type in GAME_TYPES:
    rg_cases[game_type] = 0
    control_cases[game_type] = 0
    
#iterate over df rows
for index, row in df.iterrows():
    for game_type in GAME_TYPES:
            column_name = COLUMN_PREFIX + '_' + game_type
            #check if value is not NaN
            if not np.isnan(row[column_name]):
                if (row['rg_case']) == 1:
                    rg_cases[game_type] += 1
                else:
                    control_cases[game_type] += 1

print("responsible_gamblers: ", rg_cases)
print("control", control_cases)
