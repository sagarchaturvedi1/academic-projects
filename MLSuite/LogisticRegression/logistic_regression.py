from math import log
import math
import random
import sys

#import matplotlib.pyplot as plt


weightVector = []
bias = 0
learning_rate = .1
hyper_parameter = 1
best_accuracy = 0.0
best_hyper_parameter = 0.0
w = []
bias_in_loop = 0

#===============================================================================
# def update_learning_rate(learning_rate,epoch_value,hyper_parameter):
#     l = learning_rate * (epoch_value/hyper_parameter)
#     return (learning_rate)/(1+l)
#===============================================================================

def getListParts(l, n):
    cvlist = []
    for i in range(0, len(l), n):
        cvlist.append(l[i:i + n])
    return cvlist
    
def train(training_data,plot):
    global w, bias_in_loop
    global learning_rate
    global hyper_parameter
    objective_vector = []
    for epoch in range(0,5):
        data = random.sample(training_data, len(training_data))
        obj = 0.0
        for line in data:
            rowFeatures = line.replace(" \n","").split(" ")
            y = int(rowFeatures[0])
            gradient = [0 for j in w]
            yx = [0 for j in w]
            term2 = [0 for j in w]
            dict = {}
            expo = 0.0
            for i in range(1,len(rowFeatures)):
                index = int(rowFeatures[i].split(':')[0])
                value = int(rowFeatures[i].split(':')[1])
                if index <= len(w) - 1:
                    expo += value*w[index]
            expo *= y
            expo = math.pow(2.71828,expo) + 1
            
            for i in range(len(w)):
                
                term2[i] = 2*w[i]/((hyper_parameter)**2)
            
                
            for i in range(1,len(rowFeatures)):
                index = int(rowFeatures[i].split(':')[0])
                value = int(rowFeatures[i].split(':')[1])
                dict[index] = value
                if index <= len(yx) - 1:
                    yx[index] = (y*value*-1)/expo
                
            #===================================================================
            # print('yx is', yx)
            # print(expo)
            # print('term 2 is',term2)
            #===================================================================
            
            for i in range(len(w)):
                a = yx[i] + term2[i]
                a *= learning_rate
                w[i] = w[i] - a
            
            
            if plot == 1:
                a = 0.0
                for wei in w:
                    a += wei*wei
                a /= hyper_parameter**2
                obj += (log(expo)+a)
        objective_vector.append(obj)        
        
    if plot == 1:
        print('Objective function values for all epochs',objective_vector)
        #plt.plot(objective_vector)
        #plt.ylabel("Objective function")
        #plt.show()
    
    #print('w is',w)
  
def test(test_data, printDetails):
    global best_accuracy,best_hyper_parameter
    mistakes = 0
    #print(len(test_data))
    for line in test_data:
        rowFeatures = line.replace(" \n","").split(" ")
        y = int(rowFeatures[0])
        prob = 0.0
        for i in range(1,len(rowFeatures)):
            index = int(rowFeatures[i].split(':')[0])
            value = int(rowFeatures[i].split(':')[1])
            #print(index)
            if index <= len(w) - 1:
                prob += w[index]*value
        
        prob *= -1
        prob = 1/(math.pow(2.71828,prob) + 1)
        
        if (prob >= 0.5 and y != 1) or (prob < 0.5 and y != -1):
            mistakes += 1
            
    accuracy = 1- mistakes/len(test_data)   
    
    if printDetails == 1:
        print('final accuracy in prediction ---> ',accuracy)
    
    result = {}
    result['accuracy'] = accuracy
    return result
    
def CV(cvlist):
    global weightVector,w,best_accuracy,best_hyper_parameter
    #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Starting Cross Validation >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    counter = 0
    accuracy = 0.0
    
    for test_list in cvlist:
        bias_in_loop = bias
        counter+=1
        train_d = cvlist[:]
        train_d.remove(test_list)     
        data = []
        for l in train_d:
            for m in l:
                data.append(m) 
                    
        train(data,0)
        result = test(test_list,0)
        accuracy += result['accuracy']
        w = weightVector[:]
    
    accuracy = accuracy/len(cvlist)
    #===========================================================================
    # if accuracy > best_accuracy:
    #     best_accuracy = accuracy
    #     best_hyper_parameter = hyper_parameter
    #===========================================================================
    result = {}
    result['accuracy'] = accuracy
    return result

def main():
    global weightVector, bias, learning_rate, hyper_parameter, w, best_accuracy,best_hyper_parameter,bias_in_loop
    training_data = open(sys.argv[1].strip(), 'r').readlines()
    test_data = open(sys.argv[2].strip(), 'r').readlines()
    num_of_features = int(max(training_data,key = lambda line: int(line.strip(' ').split(" ")[-2].split(":")[0])).split(" ")[-2].split(":")[0])+1

    # Initialize the weight vector
    for i in range(0,num_of_features):
            weightVector.insert(i, 0)
    bias = random.random()
    
    folds = int(sys.argv[3].strip())
    cvlist = []
    cvnumber = int(len(training_data)/folds)
    for part in getListParts(training_data, 1283):
        cvlist.append(part)
    
    print('Number of cross validation cycles', folds)
    #gamma_values = [.1,.01,.001,.0001]
    sigma_values = [1,2,5,10,20]
    
    #for gamma in gamma_values:
    for C in sigma_values:
        w = weightVector[:]
        bias_in_loop = bias

        #learning_rate = gamma
        hyper_parameter = C
        
        result = CV(cvlist)
        print('sigma parameter =',hyper_parameter,',accuracy =',result['accuracy'])

        if result['accuracy'] > best_accuracy:
            best_accuracy = result['accuracy']
            best_hyper_parameter  = hyper_parameter
        #===============================================================
        # print()
        # print()
        #===============================================================
        w=[]
        bias_in_loop = 0
    print("Best Accuracy = ", best_accuracy)
    print("Best sigma parameter = ", best_hyper_parameter)
    print()
    w = weightVector[:]
    hyper_parameter = best_hyper_parameter
    train(training_data,1)
    print()
    print("Calculating results on test data with best parameters")
    test(test_data,1)
    print()

if __name__ == '__main__':
    main()