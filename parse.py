#!/usr/bin/env python

import csv
import numpy as np
import datetime
from sklearn.svm import SVC
from sklearn.preprocessing import *
from sklearn.linear_model import LogisticRegression


#Raw extract from file train.csv : 'Miss.', 'Mme.', 'Rev.', 'Jonkheer.', 'Sir.', 'Mlle.', 'Mrs.', 'Capt.', 'Col.', 'Ms.', 'Mr.',
#'Lady.', 'Dr.', 'the', 'Master.', 'Major.', 'Don.'
#METTRE MASTER A 1 (SURVIT)
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
    return 1 if age < 10 else 0

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

                child = is_child(float(age))
                port = get_port_as_numeric(row[9 + offset])

                price = row[7 + offset] if row[7 + offset] != '' else '0'

                cabin = has_cabin(row[8+offset])
                sibsp = row[4+offset]
                parch = row[5+offset]

                #row_list.append([pclass, gender, port, price, child])
                row_list.append([pclass, gender, port, price, title, age, child, parch, sibsp])


    csvfile.close()
    return np.array(row_list, np.float)

def get_scrapped_data():
    with open('scrap.csv', 'rb') as scrap_file:
        dataset = csv.reader(scrap_file, delimiter=';')
        scrap_list = []

        for row in dataset:
            if row[0] != 'survived':
                scrap_list.append(row[0])

    scrap_file.close()

    return np.array(scrap_list,np.int)

def compute_LR(X,y,X_test):

    #for c in [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.01, 0.02, 0.03, 0.1, 0.2, 0.5, 0.7, 1, 2, 10, 100]:
    lr = LogisticRegression(C=0.02)
    #    lr = LogisticRegression(C=0.02)

    lr.fit(X,y)

    lr.transform(X)

    #Calculate accuracy
    #    print c
    print "Accuracy on X validation set : %.6f" % lr.score(X_cross_validation, y_cross_validation)

    #Calculate results for the Test set
    return lr.predict(X_test)

def compute_SVC(X,y,X_test):

    #for c in [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.01, 0.015, 0.02, 0.03, 0.1, 0.2, 0.5, 0.7, 1, 2, 10, 100,150,200]:

    svc = SVC(C=100, gamma=0.02)
    #    svc = SVC(C=100, gamma=c)
    #train the model
    svc.fit(X, y)
    #    print c
    print "Accuracy on X validation set : %.6f" % svc.score(X_cross_validation, y_cross_validation)

    return svc.predict(X_test)


X_temp = build_X_matrix('train.csv', offset=1)
X_temp = (Scaler()).fit_transform(X_temp)

X_temp = np.column_stack((np.ones((X_temp.shape[0],1),np.float), X_temp))

train_set_size = 749

X = X_temp[0:train_set_size,0::]
X_cross_validation = X_temp[train_set_size:X_temp.shape[0],0::]

y_temp = build_y_matrix('train.csv')
y = y_temp[0:train_set_size]
y_cross_validation = y_temp[train_set_size:y_temp.shape[0]]

X_test = build_X_matrix('test.csv', offset=0)
X_test = (Scaler()).fit_transform(X_test)
X_test = np.column_stack((np.ones((X_test.shape[0],1),np.float), X_test))


y_test = compute_LR(X,y,X_test)

y_scrap = get_scrapped_data()

print "Accuracy on test set : %.6f" % (y_test == y_scrap).mean()


#write the result file
with open('test.csv', 'rb') as csv_file:

    output_file = open("result/submit_nba-" +  datetime.datetime.now().strftime('%d-%m-%Y')  + ".csv", "w")

    for i, line in enumerate(csv.reader(csv_file, delimiter=','), 1):
        #skipping header
        if i >= 2:
            line.insert(0,str(int(y_test[i-2])))
            #Use double quotes to avoid incorrect columns number (due to , in names)
            line = [l.replace('\"','') for l in line]
            line = ['"' + l + '"' for l in line]
        else:
            #add the header for the survived column
            line.insert(0,'survived')

        output_file.write(",".join(line) + "\n")

    output_file.close()