import pprint

from sklearn import datasets
from sklearn import svm
from pymongo import MongoClient
mongo = MongoClient()

db = mongo.race
for docs in db.belmont_stakes.find():
    pprint.pprint(docs)
