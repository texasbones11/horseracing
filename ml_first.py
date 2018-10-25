# matplotlib
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# ML imports
import sklearn
from sklearn import linear_model
from sklearn import cross_validation
from sklearn import preprocessing

# MongoDB imports
import pprint
from pymongo import MongoClient

mongo = MongoClient()

db = mongo.workout
dirt_q = db.thoroughbred.find({"type": "Dirt"}, {"speed": 1, "distance": 1, "time": 1, "_id": 0})
df = pd.DataFrame(list(dirt_q))
# One hot encoding
# print(pd.get_dummies(df['speed']))

# ordinal numbers
# df['speed'] = df['speed'].astype('category')
# df['speed'] = df['speed'].cat.reorder_categories(
#     ['Fast', 'Wet Fast', 'Good', 'Muddy', 'Sloppy'], ordered=True)
# df['speed'] = df['speed'].cat.codes
# print(df)

# assign numbers to values
le = preprocessing.LabelEncoder()
le.fit(df['speed'])
df['speed'] = le.transform(df['speed'])
print(df['speed'])
print(le.inverse_transform(df['speed']))

# cycle through and print
# for docs in db.thoroughbred.find():
# pprint.pprint(docs)

# ML part
# drop empty strings before splitting dataset
df.replace('', np.nan, inplace=True)
df = df.dropna()
X = df.drop('time', axis=1)
Y = df.time

# print(X)
# lm = linear_model.LinearRegression()
# lm.fit(X, Y)

# view results
# print('Intercept', lm.intercept_)
# print('Number of Coeff', len(lm.coef_))

# represent coefficients
# print(pd.DataFrame(zip(X.columns, lm.coef_), columns=['features', 'estimatedCoefficients']))

# scatter plot
# plt.scatter(X.speed, df.time)
# plt.show()

# plt.scatter(X.distance, Y)
# plt.show()

# predict
# print(lm.predict(X)[0:5])
# plt.scatter(Y, lm.predict(X))
# plt.show()

# random Data test sets
X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(
    X, Y, test_size=0.33, random_state=5)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

lm = linear_model.LinearRegression()
lm.fit(X_train, Y_train)
pred_train = lm.predict(X_train)
pred_test = lm.predict(X_test)

plt.scatter(X_test.distance, pred_test)
plt.ylabel('Time (s)')
plt.xlabel('Distance (furlongs)')
plt.show()
