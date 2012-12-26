#!/usr/bin/env python

import csv
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import *
from sklearn.linear_model import LogisticRegression
import helper

def get_title_as_numeric(name):
    return {
        'Sir.': 0, 'Don.': 0, 'Mr.': 0,
        'Miss.': 1, 'Mlle.': 1, 'Ms.': 1,
        'Mme.': 2,
        'Capt.': 3, 'Col.': 3, 'Major.': 3,
        'Lady.': 1,
        'Master.' : 4,
        'Dr.' : 5,
        'Rev.' : 6,
        }.get(name, 7)

def get_gender_as_numeric(gender):
    return {
        'male':0,
        'female':1,
        }.get(gender, -1)

def get_port_as_numeric(port):
    return {
        'C':0,
        'S':1,
        'Q':2,
        }.get(port,3)

def is_child(age):
    if not has_age(age):
        return 0
    return 1 if age < 10 else 0

def has_age(age):
    return 1 if age != '' else 0


def has_cabin(cabin):
    return cabin != ''

def build_y_matrix(file):

    with open(file, 'rb') as csvfile:
        dataset = csv.reader(csvfile, delimiter=',')

        row_list = []
        for row in dataset:
            if row[0] != "survived":
                row_list.append(row[0])

    csvfile.close()
    return np.array(row_list, np.float)

# survived,pclass,name,sex,age,sibsp,parch,ticket,fare,cabin,embarked
# 0,3,"Braund, Mr. Owen Harris",male,22,1,0,A/5 21171,7.25,,S
def build_X_matrix(file, offset):
    with open(file, 'rb') as csvfile:

        dataset = csv.reader(csvfile, delimiter=',')
        row_list = []

        for row in dataset:
            #excludes the first line (header)
            if row[0 + offset] != "pclass":
                pclass = row[0 + offset]
                title = get_title_as_numeric(row[1 + offset].split(',')[1].split(' ')[1])
                gender =  get_gender_as_numeric(row[2 + offset])

                if row[3 + offset] != '':
                    age = row[3 + offset]
                else:
                    #Mean for both train et test sets
                    age = '30'

#                child = is_child(float(age))
#                port = get_port_as_numeric(row[9 + offset])

#                price = row[7 + offset] if row[7 + offset] != '' else 0

#                cabin = has_cabin(row[8+offset])
#                sibsp = row[4+offset]
#                parch = row[5+offset]

                row_list.append([pclass, gender, title, age])

    csvfile.close()
    return np.array(row_list, np.float)

def compute_LR(X,y,X_test, X_cross_validation, y_cross_validation, c):

    lr = LogisticRegression(C=c)

    lr.fit(X,y)
    lr.transform(X)

    #Calculate accuracy
    print "Accuracy on X validation set : %.6f" % lr.score(X_cross_validation, y_cross_validation)

    #Calculate results for the Test set
    return lr.predict(X_test)

def compute_SVC(X,y,X_test, X_cross_validation, y_cross_validation, c, g):

    svc = SVC(C=c, gamma=g)

    svc.fit(X, y)

    print "Accuracy on X validation set : %.6f" % svc.score(X_cross_validation, y_cross_validation)

    return svc.predict(X_test)

#deactivate feature mapping if <= 1
map_feature_degree = 3

X_temp = build_X_matrix('train.csv', offset=1)
X_temp = helper.add_polynomial_features(X_temp, map_feature_degree)
X_temp = (Scaler()).fit_transform(X_temp)
X_temp = np.column_stack((np.ones((X_temp.shape[0],1),np.float), X_temp))

train_set_size = 799

X = X_temp[0:train_set_size,0::]
X_cross_validation = X_temp[train_set_size:X_temp.shape[0],0::]

y_temp = build_y_matrix('train.csv')
y = y_temp[0:train_set_size]
y_cross_validation = y_temp[train_set_size:y_temp.shape[0]]

X_test = build_X_matrix('test.csv', offset=0)
X_test = helper.add_polynomial_features(X_test, map_feature_degree)
X_test = (Scaler()).fit_transform(X_test)
X_test = np.column_stack((np.ones((X_test.shape[0],1),np.float), X_test))

#for c in [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.01, 0.02, 0.03, 0.1, 0.2, 0.5, 0.7, 1, 2, 10, 100, 200, 500, 1000, 10000]:
#    print c
y_test = compute_LR(X,y,X_test,X_cross_validation, y_cross_validation, 10000)

y_scrap = helper.get_scrapped_data()

helper.calculate_accuracy(y_test,y_scrap)

#write the result file
helper.write_output_file(y_test)