'''
Created on Nov 14, 2016

@author: sagar
'''

import random
import sys


weightVector = []
learning_rate = 0.01
hyper_parameter = 1
best_accuracy = 0.0
best_learning_rate = 0.0
best_hyper_parameter = 0.0
w = []

def update_learning_rate(learning_rate,epoch_value,hyper_parameter):
    l = learning_rate * (epoch_value/hyper_parameter)
    return (learning_rate)/(1+l)

def add_bias_in_data(data):
    bias_data = []
    for i in range(0,len(data)):
        bias_data.append([1] + data[i])
    return bias_data

def append_labels_in_data(data,labels):
    for i in range(0,len(data)):
        data[i] = data[i].replace("\n","").strip().split(" ")
        data[i].append(labels[i].replace("\n","").strip())
    return data

def getListParts(l, n):
    cvlist = []
    for i in range(0, len(l), n):
        cvlist.append(l[i:i + n])
    return cvlist
    
def train(training_data):
    global weightVector
    global learning_rate
    global hyper_parameter
    for epoch in range(0,20):
        data = random.sample(training_data, len(training_data))
        for line in data:
            learning_rate = update_learning_rate(learning_rate, epoch, hyper_parameter)
            y = float(line[-1])
            sum = 0.0
            for i in range(0,len(line)-1):
                x = float(line[i])
                sum = sum + float(weightVector[i])*x
            sum *= y
            #print('sum is ',sum)
            if sum <= 1:
                for i in range(0,len(weightVector)):
                    weightVector[i] = ((1 - learning_rate)*weightVector[i])+(learning_rate*hyper_parameter*y*float(line[i]))
            else:
                for i in range(0,len(weightVector)):
                    weightVector[i] = (1 - learning_rate)*weightVector[i]
    
    #print('final weight vector after training --->',weightVector)

def test(test_data, printDetails, evaluation_measure):
    global best_accuracy,best_hyper_parameter,best_learning_rate
    mistakes = 0
    tp = 0
    fp = 0
    fn = 0
    #print(len(test_data))
    for line in test_data:
        y = int(line[-1])
        sum = 0.0
        for i in range(0,len(line)-1):
            x = float(line[i])
            sum = sum + float(weightVector[i])*x
        sum *= y
        if sum < 0:
            mistakes += 1
            if y == 1:
                fn += 1
            else:
                fp += 1
        elif y == 1:
            tp += 1
            
    accuracy = 1- mistakes/len(test_data)
    precision = 0.0
    recall = 0.0
    f1 = 0.0
    
    if tp+fp > 0:
        precision = tp/(tp+fp)   
    if tp+fn > 0:
        recall = tp/(tp+fn)
    if precision + recall > 0:
        f1 = (2 * precision * recall)/(precision + recall)
    
    if printDetails == 1:
        if evaluation_measure.lower() == 'prf':
            print('precision =',precision,',recall =',recall,',F1 =',f1)
        else:
            print('final accuracy in prediction ---> ',accuracy)
    
    result = {}
    result['accuracy'] = accuracy
    result['precision'] = precision
    result['recall'] = recall
    result['f1'] = f1
    return result
    
def CV(cvlist,evaluation_measure):
    global weightVector
    #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Starting Cross Validation >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    counter = 0
    accuracy = 0.0
    precision = 0.0
    recall = 0.0
    f1 = 0.0
    
    for test_list in cvlist:
        counter+=1
        train_d = cvlist[:]
        train_d.remove(test_list)     
        data = []
        for l in train_d:
            for m in l:
                data.append(m) 
                    
        train(data)
        result = test(test_list,0,evaluation_measure)
        accuracy += result['accuracy']
        precision += result['precision']
        recall += result['recall']
        f1 += result['f1']
        weightVector = w[:]
    
    accuracy = accuracy/len(cvlist)
    precision = precision/len(cvlist)
    recall = recall/len(cvlist)
    f1 = f1/len(cvlist)
    result = {}
    result['accuracy'] = accuracy
    result['precision'] = precision
    result['recall'] = recall
    result['f1'] = f1
    return result

def main():
    global weightVector, learning_rate, hyper_parameter, w, best_accuracy,best_hyper_parameter,best_learning_rate
    exp_type = sys.argv[1].strip()
    training_data = open(sys.argv[2].strip(), 'r').readlines()
    test_data = open(sys.argv[3].strip(), 'r').readlines()
    train_labels = open(sys.argv[2].strip().replace('.data','.labels'), 'r').readlines()
    test_labels = open(sys.argv[3].strip().replace('.data','.labels'), 'r').readlines()
    training_data = add_bias_in_data(append_labels_in_data(training_data, train_labels))
    test_data = add_bias_in_data(append_labels_in_data(test_data, test_labels))
    num_of_features = len(training_data[0]) - 1

    # Initialize the weight vector
    for i in range(0,num_of_features):
        weightVector.insert(i, 0)
    
    w = weightVector[:]
    if exp_type.lower() == 'svm':
        evaluation_measure = sys.argv[4].strip()
        train(training_data)
        test(test_data,1,evaluation_measure)
        
    if exp_type.lower() == 'cv':      
        folds = int(sys.argv[4].strip())
        evaluation_measure = sys.argv[5].strip()
        cvlist = []
        for part in getListParts(training_data, int(len(training_data)/folds)):
            cvlist.append(part)
        
        gamma_values = [.1,.01,.001,.0001]
        C_values = [2,1,.5,.25,.125,.0625]
        
        for gamma in gamma_values:
            for C in C_values:
                learning_rate = gamma
                hyper_parameter = C
                
                result = CV(cvlist,evaluation_measure)
                if evaluation_measure.lower() == 'prf':
                    print('learning_rate =',gamma,',C =',hyper_parameter,',precision ='
                          ,result['precision'],',recall =',result['recall'],',F1 =',result['f1'])
                else:
                    print('learning_rate =',gamma,',C =',hyper_parameter,',accuracy =',result['accuracy'])
                
                if result['accuracy'] > best_accuracy:
                    best_accuracy = result['accuracy']
                    best_learning_rate = gamma
                    best_hyper_parameter  = hyper_parameter
                #===============================================================
                # print()
                # print()
                #===============================================================
                
        print("Best Accuracy = ", best_accuracy)
        print("Best hyper-parameter = ", best_hyper_parameter)
        print("Best learning rate = ", best_learning_rate)
        print()
        
        print("Calculating results on training data with best parameters")
        learning_rate = best_learning_rate
        hyper_parameter = best_hyper_parameter
        train(training_data)
        test(training_data,1,evaluation_measure)
        print()
        print("Calculating results on test data with best parameters")
        test(test_data,1,evaluation_measure)
        print()

if __name__ == '__main__':
    main()