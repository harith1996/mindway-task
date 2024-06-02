import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
import scipy.stats as stats



df = pd.read_csv('Gambling_data.csv', sep=";")

#selecting the columns
sub_df = df[df.columns[8:].union(['rg_case'])]
le = preprocessing.LabelEncoder()
df['country_name'] = le.fit_transform(df['country_name'])
df['language_name'] = le.fit_transform(df['language_name'])
df['gender'] = le.fit_transform(df['gender'])
feat_importance = []
for c in df.columns[8:].union(['rg_case', 'country_name', 'language_name', 'gender']):
    df.dropna(subset=[c, 'rg_case'], inplace=True)
    corr = stats.pointbiserialr(df['rg_case'], df[c])
    feat_importance.append({
        'column': c,
        'correlation': corr[0],
        'p-value': corr[1]
    })
    #sort by correlation
feat_importance = pd.DataFrame(sorted(feat_importance, key=lambda x: abs(x['correlation']), reverse=True))
print(feat_importance)
# #sort by absolute value
# rg_case_corr = rg_case_corr.reindex(rg_case_corr.abs().sort_values(ascending=False).index)
# print(rg_case_corr)