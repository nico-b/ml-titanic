#!/usr/bin/env python

import csv
import sys
import sklearn

#Raw extract from file train.csv : 'Miss.', 'Mme.', 'Rev.', 'Jonkheer.', 'Sir.', 'Mlle.', 'Mrs.', 'Capt.', 'Col.', 'Ms.', 'Mr.',
#'Lady.', 'Dr.', 'the', 'Master.', 'Major.', 'Don.'
def getTitleAsNumeric(name):
    return {
    	'Miss.': '1', 'Mlle.': '1', 'Ms.': '1',
    	'Mme.': '2',
    	'Sir.': '3', 'Don.': '3',
    	'Mr.': '4',
    	'Capt.': '5', 'Col.': '5', 'Major.': '5',
    	'Lady.': '6',
		'Dr.' : '7', 'Master.' : '7',
		'Rev.' : '8',
	}.get(name, '9')

def getGenderAsNumeric(gender):
	return {
		'male':'0',
		'female':'1',
	}.get(gender, '-1')

def getPortAsNumeric(port):
	return {
		'C':'1',
		'Q':'2',
		'S':'3',
	}.get(port,'4')

#ignore parch for the first version, check only by age	
def isChild(age):
	 return '1' if age < 15 else '0'    
	

# survived,pclass,name,sex,age,sibsp,parch,ticket,fare,cabin,embarked
# 0,3,"Braund, Mr. Owen Harris",male,22,1,0,A/5 21171,7.25,,S

#First version, we only keep : pclass, title extracted from name, sex (gender), isChild extracted from age, age, port
with open(sys.argv[1], 'rb') as csvfile:
	
	dataset = csv.reader(csvfile, delimiter=',')
	fileType = sys.argv[1].split('.')[0]
	outputFile = open("octave/" + fileType + "_output.csv", "w")
    
	#default value for test set
	offset = 0
	
	if fileType == 'train':
		offset = 1

	for row in dataset:
		#excludes the first line and also lines with no age
		if row[0 + offset] != "pclass":
			pclass = row[0 + offset]
			title = getTitleAsNumeric(row[1 + offset].split(',')[1].split(' ')[1])
			gender =  getGenderAsNumeric(row[2 + offset])
				
			if row[3 + offset] != '':
				age = row[3 + offset]
			else:
				#Mean for both train et test sets
				age = '30'
			
			child = isChild(int(float(age)))
			port = getPortAsNumeric(row[9 + offset])
			
			price = row[7 + offset] if row[7 + offset] != '' else '0'
			
			if offset == 0:
				line = ','.join(filter(None, (gender)))
				#line = ','.join(filter(None, (pclass, title, gender, child, age, port)))
			elif offset == 1:
				exactResult = row[0]
				line = ','.join(filter(None, (exactResult, gender)))
				#line = ','.join(filter(None, (exactResult, pclass, title, gender, child, age, port)))
			outputFile.write(line + '\n')

	csvfile.close()
	outputFile.close()
	
from sklearn.svm import SVC
clf = SVC()
clf.fit(X, y)