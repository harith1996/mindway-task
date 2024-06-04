#find the most important features to predict rg_case
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn import preprocessing
from matplotlib import pyplot as plt


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

# define and fit the models
random_for = RandomForestClassifier()
xgb = XGBClassifier()
random_for.fit(X, y)
xgb.fit(X, y)

# get importances
random_for_imp = random_for.feature_importances_
xgb_imp = xgb.feature_importances_

# summarize feature importance
for i,v in enumerate(random_for_imp):
    column = df.columns[i]
    print('Feature: %0d, Score: %.5f' % (i,v), column)

for i,v in enumerate(xgb_imp):
    column = df.columns[i]
    print('Feature: %0d, Score: %.5f' % (i,v), column)

# plot feature importance for both in one plot
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16, 8))
plt.subplot(2, 1, 1)
plt.bar([df.columns[x] for x in range(len(random_for_imp))], random_for_imp)
plt.xticks(rotation=90)

plt.subplot(2, 1, 2)
plt.bar([df.columns[x] for x in range(len(xgb_imp))], xgb_imp)
plt.xticks(rotation=90)
plt.show()
