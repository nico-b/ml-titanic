#!/usr/bin/env python

import csv
import sys
import sklearn
import numpy as np
import datetime
from sklearn.svm import SVC
from sklearn.preprocessing import *
from sklearn.linear_model import LogisticRegression


#Raw extract from file train.csv : 'Miss.', 'Mme.', 'Rev.', 'Jonkheer.', 'Sir.', 'Mlle.', 'Mrs.', 'Capt.', 'Col.', 'Ms.', 'Mr.',
#'Lady.', 'Dr.', 'the', 'Master.', 'Major.', 'Don.'
def get_title_as_numeric(name):
    return {
		'Sir.': 0, 'Don.': 0, 'Mr.': 0,
    	'Miss.': 1, 'Mlle.': 1, 'Ms.': 1, 'Lady.': 1,
    	'Mme.': 2,
    	'Capt.': 3, 'Col.': 3, 'Major.': 3, 'Jonkheer.':3, 'Rev.' :3,
		'Dr.' : 4, 'Master.' : 4,
	}.get(name, 6)

def get_gender_as_numeric(gender):
	return {
		'male':0,
		'female':1,
	}.get(gender, -1)

def get_port_as_numeric(port):
	return {
		'C':1,
		'S':0,
		'Q':0,
	}.get(port,1)


def is_child(age):
	 return 1 if age < 8 else 0    
	
def has_cabin(cabin):
	return cabin != ''
	
def get_cabin_as_numeric(cabin):
	return {
		'A':0,
		'B':1, 'C':1, 'D':1, 'E':1, 'F':1,
	}.get(cabin, 0)	
	
def has_big_sibsp(sibsp):
	return sibsp < 3

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
				
				age = 0
				if row[3 + offset] != '':
					age = row[3 + offset]
				else:
					#Mean for both train et test sets
					age = '30'
			
				child = is_child(float(age))
				port = get_port_as_numeric(row[9 + offset])
			
				price = row[7 + offset] if row[7 + offset] != '' else '0'
				
				hascabin = has_cabin(row[8+offset])
				sibsp = has_big_sibsp(row[4+offset])
				parch = row[5+offset]
				cabin = get_cabin_as_numeric(row[8+offset][0] if row[8+offset] != '' else '')
                
				#tendance a l'overfitting avec C trop bas : performe a 0.8565 avec C=1  
				row_list.append([pclass, gender, port, price, title, age, child, parch, cabin])

	csvfile.close()
	return np.array(row_list, np.float)

def compute_LR(X,y,X_test):
	normalize(X)
    
	#for c in np.linspace(0.01,1,1000):
	lr = LogisticRegression(C=1)
		#lr = LogisticRegression(C=c, tol=0.00000001)
	lr.fit(X,y)

	lr.transform(X)

	#Calculate accuracy
	#print lr.predict(X_cross_validation)
		#print c
	print "Accuracy : %.6f" % lr.score(X_cross_validation, y_cross_validation)

	#Calculate results for the Test set
	return lr.predict(X_test) 

def compute_SVC(X,y,X_test):

	svc = SVC(C=2, gamma=0.016)
	#train the model
	svc.fit(X, y)

	print "Accuracy : %.6f" % svc.score(X_cross_validation, y_cross_validation)
	
	return svc.predict(X_test)	
	
X_temp = build_X_matrix('train.csv', offset=1)
X_temp = np.column_stack((np.ones((X_temp.shape[0],1),np.float), X_temp))
X = X_temp[0:799,0::]
X_cross_validation = X_temp[799:X_temp.shape[0],0::]

y_temp = build_y_matrix('train.csv')
y = y_temp[0:799]
y_cross_validation = y_temp[799:y_temp.shape[0]]

X_test = build_X_matrix('test.csv', offset=0)
X_test = np.column_stack((np.ones((X_test.shape[0],1),np.float), X_test))

y_test = compute_LR(X,y,X_test)

#write the result file
with open('test.csv', 'rb') as csvfile:

	dataset = csv.reader(csvfile, delimiter=',')
	
	output_file = open("result/submit_nba-" +  datetime.datetime.now().strftime('%d-%m-%Y')  + ".csv", "w")
	
	for i, line in enumerate(dataset, 1):
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
