# ###################
# Data pull from MongoDB
from pymongo import MongoClient
import pprint
mongo = MongoClient()

db = mongo.thoroughbred
pipeline = [{"$unwind": "$name"},
            {"$lookup": {"from": "earnings", "localField": "name", "foreignField": "name", "as": "earnings"}},
            {"$lookup": {"from": "current", "localField": "name", "foreignField": "name", "as": "current"}},
            {"$replaceRoot": {"newRoot": {"$mergeObjects": [
                {"$arrayElemAt": ["$current", 0]}, "$$ROOT"]}}},
            {"$project": {"current": 0}},
            {"$match": {"workouts": {"$ne": []}}}]
m_query = db.workouts.aggregate(pipeline)
# pprint.pprint(list(m_query))

# ###################
# Preprocess data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(list(m_query))
print(list(df))
df1 = df[['age', 'date', 'distance', 'earnings', 'notes',
          'race', 'sex', 'speed', 'time', 'track', 'type']]

print(df1['earnings'][1])

# print(list(df1))
df1 = df1[df1.astype(str)['earnings'] != '[]']

# remove space in notes:
df1['notes'] = df1['notes'].replace(' ', '', regex=True)

df2 = df1[['age', 'distance', 'notes', 'race', 'sex', 'speed', 'time', 'track', 'type']]

df2['race'].replace('', 'Raced', inplace=True)
df2.replace('', np.nan, inplace=True)
df2 = df2.dropna()

# assign numbers to values
from sklearn import preprocessing
from sklearn.preprocessing import LabelBinarizer

enc = preprocessing.OneHotEncoder()
le = preprocessing.LabelEncoder()

# df3 = df2[['notes', 'time']]

df2 = df2[['sex', 'type', 'time', 'distance', 'speed', 'race', 'age', 'notes']]
# view how many of each catagory
print(df2.groupby('type').nunique())
# n ominal datasets:
df2['sex'] = df2['sex'].astype('category')
df2['notes'] = df2['notes'].astype('category')
df2['race'] = df2['race'].astype('category')
df2['type'] = df2['type'].astype('category')
df2['speed'] = df2['speed'].astype('category')
df2 = pd.get_dummies(df2, columns=['sex', 'type', 'race', 'notes', 'speed'])

# ordinal datasets:
# scale_mapper = {'Fast': 1, 'Firm': 2, 'Wet Fast': 3,
#                'Good': 4, 'Sloppy': 5, 'Muddy': 6, 'Yielding': 7}
#df2['speed'] = df2['speed'].replace(scale_mapper)

# avoid dummy trap
df2.drop('notes_b', axis=1, inplace=True)
df2.drop('sex_F', axis=1, inplace=True)
df2.drop('speed_Fast', axis=1, inplace=True)
df2.drop('type_Turf', axis=1, inplace=True)
df2.drop('race_Raced', axis=1, inplace=True)
print(df2)
# place into X and Y
X = df2.drop('time', axis=1)
Y = df2.time

# ###################
# Split Data sets
from sklearn import cross_validation

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
    X, Y, test_size=0.2, random_state=5)


from sklearn import linear_model

lm = linear_model.LinearRegression()
model = lm.fit(X_train, Y_train)
pred_train = lm.predict(X_train)
pred_test = lm.predict(X_test)

print(model.coef_)
# R2 score - closer to 1 the better
print('R2 Score: ')
print(model.score(X_test, Y_test))
# MSE - average amount off by
print('MSE: ')
print(np.mean((model.predict(X_test) - Y_test) ** 2))
# sum of all MSE's
print('MSE Sum: ')
print(((Y_test - model.predict(X_test)) ** 2).sum())
