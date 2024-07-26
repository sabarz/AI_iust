\\\\\\\\\\\\\\import math
import numpy as np
from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import random

# Naive Bayes Classifier : 

#First we separate our data by class name of flower :

def sep_class(data) :
    sep = dict()
    for i in range(len(data)):
        vector = data[i]
        value = vector[-1]
        if value not in sep :
            sep[value] = []
        sep[value].append(vector)
    return sep


# find avrg of data :
def avg(data) :
    return sum(data)/float(len(data))


#deviation : 
def dev(data) :
    average = avg(data)
    variance = sum([(x-average)**2 for x in data]) / float(len(data)-1)
    return math.sqrt(variance)

# gather each data with average and deviation :
def final_dataset(data) :
    for i in range(len(data)) :
        data[i] = data[i][:-1]
    final = [(avg(column),dev(column),len(column))for column in zip(*data)]
    del final[-1]
    return final


#gather data and sep by class :
def final_by_class(dataset):
    separated = sep_class(dataset)
    final = dict()
    for class_value, rows in separated.items():
        final[class_value] = final_dataset(rows)
    return final

#Gaussian PDF : 
def prob(x,avg,dev) :
    expp = math.exp(-((x-avg)**2 / (2*dev**2)))
    return (1/(math.sqrt(2*math.pi)*dev)) * expp


#probabilities of predicting each class for a given example
def classes_prob(final,example) :
    total_rows = sum([final[label][0][2] for label in final])
    probs = dict()
    for class_value, class_final in final.items() :
        probs[class_value] = final[class_value][0][2]/float(total_rows)
        for i in range(len(class_final)) :
            avg,dev,count = class_final[i]
            probs[class_value] *= prob(example[i],avg,dev)
    return probs

#predict class for one example :
def predict(final,example) :
    probs = classes_prob(final,example)
    result_class = None
    result_prob = -1
    for class_value,prob in probs.items() :
        if prob > result_prob :
            result_prob = prob
            result_class = class_value
    return result_class

#apply train data and test data :
def naive(train,test) :
    full_nums = len(test)
    full_correct_predict = 0
    final = final_by_class(train)
    classes = list(final.keys())
    class_correct_predict = [0,0,0]
    class_nums = [0,0,0]
    predictions = []
    for example in test :

        prd = predict(final,example)
        if example[-1] == classes[0] :
            class_nums[0]+=1
        elif example[-1] == classes[1] :
            class_nums[1]+=1
        elif example[-1] == classes[2] :
            class_nums[2]+=1

        if prd == example[-1] :
            full_correct_predict+=1
            if example[-1]==classes[0] :
                class_correct_predict[0]+=1
            elif example[-1]==classes[1] :
                class_correct_predict[1]+=1
            elif example[-1]==classes[2] :
                class_correct_predict[2]+=1
        predictions.append(prd)
    #full and class Accurancy :
    print("full Accuracy of my Naive Bayes : ",100*(full_correct_predict/full_nums))
    for i in range(len(classes)) :
        print("Accuracy of class =",classes[i],":",100*(class_correct_predict[i]/class_nums[i]))


#now test the Naive Bayes on Iris data : 


#Q1 : 
#Based on Question we use 80% of data for train and 20% of data for test :

iris = open("./iris.data")
iris = list(iris)
data = []

for i in range(len(iris)) :
    if i==len(iris)-1:
        break
    example = iris[i].split(",")
    example[-1] = example[-1][:-1]
    example[0] = float(example[0])
    example[1] = float(example[1])
    example[2] = float(example[2])
    example[3] = float(example[3])
    data.append(example)

train = random.sample(data, k=round(len(data) * 0.8))
test = []
for i in range(len(data)) :
    if data[i] not in train :
        test.append(data[i])

naive(train,test)

#Q3 : Compare to scikit-learn :

X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=0)
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)
print("accuracy of scikit : ", 100*(y_test == y_pred).sum()/X_test.shape[0])

#Baktash Ansari