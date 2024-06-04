# find the most important features to predict rg_case
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn import preprocessing
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# categorical columns
CAT_COLS = ["country_name", "language_name", "gender"]

# date columns
DATE_COLS = ["first_deposit_date", "registration_date"]


def preprocess(df):
    # transform categorical to numerical
    le = preprocessing.LabelEncoder()
    for col in CAT_COLS:
        df[col] = le.fit_transform(df[col])

    # transform date to month
    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].dt.month

    return df


def get_feature_importance(model, X, y):
    model.fit(X, y)
    return model.feature_importances_


def print_feature_importance(importances, columns):
    for i, v in enumerate(importances):
        column = columns[i]
        print("Feature: %0d, Score: %.5f" % (i, v), column)

if __name__ == "__main__":
    
    main_df = pd.read_csv("Gambling_data.csv", sep=";")

    # remove target variable
    df = main_df.drop(columns=["rg_case"])
    df = preprocess(df)

    # transform sub_df to numpy array
    X = df.to_numpy()

    # extract the target variable
    y = main_df["rg_case"].to_numpy()

    # define and fit the models
    random_for = RandomForestClassifier()
    xgb = XGBClassifier()

    # get importances
    random_for_imp = get_feature_importance(random_for, X, y)
    xgb_imp = get_feature_importance(xgb, X, y)

    # summarize feature importance
    print_feature_importance(random_for_imp, df.columns)
    print_feature_importance(xgb_imp, df.columns)

    fig = make_subplots(rows=1, cols=3)

    fig.add_trace(
        go.Bar(
            x=[df.columns[x] for x in range(len(random_for_imp))],
            y=random_for_imp,
            name="Random Forest",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=[df.columns[x] for x in range(len(xgb_imp))], y=xgb_imp, name="XGBoost"),
        row=1,
        col=2,
    )

    fig.update_layout(height=600, width=1500, title_text="Side By Side Feature Importance")
    fig.show()
