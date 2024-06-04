import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
import scipy.stats as stats
from part_1_task_2 import preprocess, get_feature_importance, print_feature_importance
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_csv('Gambling_data.csv', sep=";")
GAME_TYPES = ['fixedodds', 'liveaction', 'casino']
COLUMN_PREFIX = 'duration'

def filter_by_game_type(game_type:str):
    """Return players that play ONLY the specified game type

    Args:
        game_type (str): _description_
    """
    game_type_column = COLUMN_PREFIX + '_' + game_type
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df[game_type_column].notnull()]
    #remove columns of other game types
    for g in GAME_TYPES:
        if g != game_type:
            filtered_df = filtered_df.dropna(subset=[COLUMN_PREFIX + '_' + g])
            droppable_columns = list(filter(lambda x : g in x, df.columns))
            filtered_df = filtered_df.drop(columns=droppable_columns)
    return filtered_df

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

print("rg_cases: ", rg_cases)
print("non_rg_cases", control_cases)

fig = make_subplots(rows=1, cols=3)

for i, game_type in enumerate(GAME_TYPES):
    # get feature importance
    X = filter_by_game_type(game_type)
    X = preprocess(X)
    y = X['rg_case']
    X = X.drop(columns=['rg_case'])
    columns = X.columns
    X = X.to_numpy()
    y = y.to_numpy()
    model = XGBClassifier()
    feature_importance = get_feature_importance(model, X, y)
    print_feature_importance(feature_importance, columns)

    fig.add_trace(
        go.Bar(
            x=[columns[x] for x in range(len(feature_importance))],
            y=feature_importance,
            name=game_type,
        ),
        row=1,
        col=i+1,
    )

fig.update_layout(height=600, width=1500, title_text="Feature importance (XGBoost) by game type")
fig.show()
