# -*- coding: utf-8 -*-
"""BodyFatEstimator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_a-x_ew1GG9PyfgoCcdJjWO7ATy39M-w
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

df = pd.read_csv('bodyfat.csv')
df.head()

df.info()

# checking which columns are helpful to predict the the result
def plotdistplz(col):
  plt.figure(figsize=(12,5))
  sn.kdeplot(df['BodyFat'], color = 'blue',label='BodyFat')
  sn.kdeplot(df[col], color = 'red',  label=col)
  plt.legend()
  plt.show()

cols = list(df.columns)
for i in cols:
  print(f'Distribution plots for {i} feature is shown below')
  plotdistplz(i)
  print('-'*100)

"""from above distribution plot we can consider the most reliable data which will help to predict data"""

# check data is distributed centraly or not

import scipy.stats as stats

def drawplots(df,col):
  plt.figure(figsize=(15,7))
  plt.subplot(1,3,1)
  plt.hist(df[col], color='blue')

  plt.subplot(1,3,2)
  stats.probplot(df[col], dist='norm', plot=plt)

  plt.subplot(1,3,3)
  sn.boxenplot(data = df[col], orient='h', color = 'blue')

  plt.show()

cols = list(df.columns)

for i in cols:
  print(f'Distribution plots for the feature {i} are shown below')
  drawplots(df,i)
  print('-'*100)

"""we can see that every data is centraly distributed"""

#checking outliers

upperlimit = []
lowerlimit = []
for i in df.columns:
  upperlimit.append(df[i].mean()+(df[i].std())*4)
  lowerlimit.append(df[i].mean()-(df[i].std())*4)

cols= list(df.columns)
j=0
for i in cols:
  temp = df.loc[(df[i]>upperlimit[j])&(df[i]<lowerlimit[j])]

temp

"""This means there is no out liers"""

#using extratrees regressor for feature selction

data =  df.copy()
y = data['BodyFat']
X = data.drop(['BodyFat'], axis = 1)

from sklearn.ensemble import ExtraTreesRegressor
er = ExtraTreesRegressor()
er.fit(X,y)

series = pd.Series(er.feature_importances_,index=X.columns)
series.nlargest(5).plot(kind = 'barh', color = 'red')

# Using Mutual Information gain for feature selection

from sklearn.feature_selection import mutual_info_regression
mr = mutual_info_regression(X, y)

plotdata = pd.Series(mr, index=X.columns)
plotdata.nlargest(5).plot(kind = 'barh', color = 'red')

"""Removing correlation"""

data

plt.figure(figsize=(15,7))
sn.heatmap(df.corr(), annot=True,cmap='plasma')

def correlation(df, threshold):
  colcor = set()

  cormat = df.corr()

  for i in range(len(cormat)):
    for j in range(i):

      if abs(cormat.iloc[i][j]) > threshold:
        colname = cormat.columns[i]
        colcor.add(colname)
  return colcor

ans = correlation(X, threshold = 0.85)
ans

columns = ['Density','Chest','Abdomen','Weight','Hip']

X_new = X[columns]

X_new

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.5, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 8, random_state = 0)
regressor.fit(X_train.values, y_train)

y_pred = regressor.predict(X_test.values)
np.set_printoptions(precision=0)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.values.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)

X_new = X[columns]
y = data['BodyFat']
predicted = regressor.predict(X_new.values)

X_new['Actual Result'] = y
X_new['Predicted Result'] = predicted
X_new

sn.distplot(X_new['Actual Result'], label = 'Actual Result', hist=False, color = 'blue')
sn.distplot(X_new['Predicted Result'], label = 'Predicted Result', hist=False, color = 'Red')

r2_score(X_new['Actual Result'],X_new['Predicted Result'])

import pickle
file = open('bodyfatmodel.pkl','wb')
pickle.dump(regressor, file)
file.close()

p = regressor.predict([[1,100,100,100,100]])

p