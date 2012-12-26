#!/usr/bin/env python
import csv
import datetime
import numpy as np

def calculate_accuracy(y_test,y_scrap):

    max_accuracy_test = 0
    reg_factor = 0
    curr_accuracy_test = (y_test == y_scrap).mean()

    if curr_accuracy_test > max_accuracy_test:
        max_accuracy_test = curr_accuracy_test
        #    reg_factor = c
    #print "\nRegularization factor : %.6f" % reg_factor
    print "Accuracy on test set : %.6f" % max_accuracy_test

def add_polynomial_features(X, degree):
    m, n = X.shape
    out = X

    if degree >= 2:
        # Add ^2 features.
        for i in range(n):
            for j in range(i, n):
                out = np.hstack((out, X[:, i].reshape(m, 1) * X[:, j].reshape(m, 1)))

    if degree >=3:

        # Add ^3 features.
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    out = np.hstack(
                        (out, X[:, i].reshape(m, 1) * X[:, j].reshape(m, 1) * X[:, k].reshape(m, 1)))

    if degree >=4:
        # Add ^4 features.
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    for l in range(k,n):
                        out = np.hstack(
                            (out, X[:, i].reshape(m, 1) * X[:, j].reshape(m, 1) * X[:, k].reshape(m, 1) * X[:, l].reshape(m, 1)))

    return out


#write the output result file
def write_output_file(y_test):
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