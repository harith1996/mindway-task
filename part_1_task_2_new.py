#find the most important features to predict rg_case
import pandas as pd
import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import preprocessing
from matplotlib import pyplot


main_df = pd.read_csv('Gambling_data.csv', sep=";")

#remove target variable
df = main_df.drop(columns=['rg_case'])

#categorical columns
CAT_COLS = ['country_name', 'language_name', 'gender']

#date columns
DATE_COLS = ['first_deposit_date', 'registration_date']

#transform categorical to numerical
le = preprocessing.LabelEncoder()
for col in CAT_COLS:
    df[col] = le.fit_transform(df[col])

#transform date to month
for col in DATE_COLS:
    df[col] = pd.to_datetime(df[col])
    df[col] = df[col].dt.month

#transform sub_df to numpy array
X = df.to_numpy()

# extract the target variable
y = main_df['rg_case'].to_numpy()

# define and fit the model
model = RandomForestClassifier()
model.fit(X, y)

# get importance
importance = model.feature_importances_

# summarize feature importance
for i,v in enumerate(importance):
    column = df.columns[i]
    print('Feature: %0d, Score: %.5f' % (i,v), column)

# plot feature importance
pyplot.bar([df.columns[x] for x in range(len(importance))], importance)
pyplot.title('Feature Importance for responsible gambling')
pyplot.xticks(rotation=90)
pyplot.show()
