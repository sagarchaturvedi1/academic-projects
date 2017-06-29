'''
Created on Sep 22, 2016

@author: sagar
'''
import sys
import random

weightVector = []
bias = 0
learning_rates = [.01,.1,.3,.5,1]
margins = [0,.5,1,3,5]
epochs = [3,5]
best_accuracy = 0
best_margin = 0
best_learning_rate = 0
best_learning_rate_normal = 0
best_accuracy_normal = 0
w = []
bias_in_loop = 0

def trainPerceptron(training_data, learning_rate):
    global weightVector,bias
    mistakes = 0
    for line in training_data:
        rowFeatures = line.replace(" \n","").split(" ")
        y = int(rowFeatures[0])
        sum = 0
        dict = {}
        for i in range(1,len(rowFeatures)):
            index = int(rowFeatures[i].split(':')[0])
            value = int(rowFeatures[i].split(':')[1])
            dict[index] = value
            sum += weightVector[index]*value
        sum += bias
        sum *= y
        #print('sum is ',sum)
        if sum <= 0:
            mistakes += 1
            bias += learning_rate*y
            for key, value in dict.items():
                weightVector[int(key)] = weightVector[int(key)] + learning_rate*y*int(value)
 
    print('number of updates made during training ---> ',mistakes)
    print('final weight vector after training --->',weightVector)
    print('final bias after training --->',bias)

def trainMarginPerceptron(training_data, learning_rate, margin, printDetails, epoch, shuffleData):
    if epoch > 0:
        for x in range(0,epoch):
            print("------------------------------------------ Epoch round = ",x+1, 
                              " ----------------------------------------------------------")
            data = training_data[:]
            if shuffleData == 1:        
                data = random.sample(training_data, len(training_data))
            if learning_rate == 0:
                trainAggressivePerceptron(data, margin, printDetails)               
            else:
                train(data, learning_rate, margin, printDetails)
    else:
        if learning_rate == 0:
            trainAggressivePerceptron(training_data, margin, printDetails)               
        else:
            train(training_data, learning_rate, margin, printDetails)
    
def train(training_data, learning_rate, margin, printDetails):
    global w,bias_in_loop
    mistakes = 0
    for line in training_data:
            rowFeatures = line.replace(" \n","").split(" ")
            y = int(rowFeatures[0])
            sum = 0
            dict = {}
            for i in range(1,len(rowFeatures)):
                index = int(rowFeatures[i].split(':')[0])
                value = int(rowFeatures[i].split(':')[1])
                dict[index] = value
                sum += w[index]*value
            sum += bias_in_loop
            sum *= y
            #print('sum is ',sum)
            if sum <= margin:
                mistakes += 1
                bias_in_loop += learning_rate*y
                for key, value in dict.items():
                    w[int(key)] = w[int(key)] + learning_rate*y*int(value)
    if printDetails == 1:
        print('number of updates made during training ---> ',mistakes)
    #print('final weight vector after training --->',w)
    #print('final bias after training --->',bias_in_loop)

def trainAggressivePerceptron(training_data, margin, printDetails):
    global w,bias_in_loop
    mistakes = 0
    for line in training_data:
            rowFeatures = line.replace(" \n","").split(" ")
            y = int(rowFeatures[0])
            sum = 0
            dict = {}
            for i in range(1,len(rowFeatures)):
                index = int(rowFeatures[i].split(':')[0])
                value = int(rowFeatures[i].split(':')[1])
                dict[index] = value
                sum += w[index]*value
            sum += bias_in_loop
            sum *= y
            #print('sum is ',sum)
            if sum <= margin:
                mistakes += 1
                learning_rate = (margin - sum)
                mul = 0
                for value in dict.values():
                    mul = mul + value*value
                learning_rate /= (mul+1)
                #print(learning_rate)
                bias_in_loop += learning_rate*y
                for key, value in dict.items():
                    w[int(key)] = w[int(key)] + learning_rate*y*int(value)
    if printDetails == 1:
        print('number of updates made during training ---> ',mistakes)
    
def testPerceptron(test_data,learning_rate,margin, printDetails):
    global best_accuracy,best_learning_rate,best_margin,best_accuracy_normal,best_learning_rate_normal
    print('----------------------------------------------------------------------------------')
    mistakes = 0
    for line in test_data:
        rowFeatures = line.replace(" \n","").split(" ")
        y = int(rowFeatures[0])
        sum = 0
        for i in range(1,len(rowFeatures)):
            index = int(rowFeatures[i].split(':')[0])
            value = int(rowFeatures[i].split(':')[1])
            #print(index)
            if index <= len(w) - 1:
                sum += w[index]*value
        sum += bias_in_loop
        sum *= y
        #print('sum is ',sum)
        if sum < 0:
            mistakes += 1
    
    accuracy = 1- mistakes/len(test_data)
    if margin == 0:
        if accuracy > best_accuracy_normal:
            best_accuracy_normal = accuracy
            best_learning_rate_normal = learning_rate
    elif accuracy > best_accuracy:
        best_accuracy = accuracy
        best_learning_rate = learning_rate
        best_margin  = margin
    
    if printDetails == 1:
        print('number of mistakes in prediction ---> ',mistakes)
        print('final accuracy in prediction ---> ',accuracy)
    print()
                   
if __name__ == '__main__':
    global weightVector,bias
    exp_type = sys.argv[1]
    training_file = open(sys.argv[2], 'r')
    training_data = training_file.readlines()
    count = -1
    test_file = []
    test_data = []
    if exp_type.lower() != 'exp1':
        count = -2
        test_file = open(sys.argv[3], 'r')
        test_data = test_file.readlines()
    num_of_features = int(max(training_data,key = lambda line: int(line.strip(' ').split(" ")[count].split(":")[0])).split(" ")[count].split(":")[0])+1
    featureVector = {}
    if exp_type.lower() == 'exp1':
        for i in range(0,num_of_features):
                weightVector.insert(i, 0)
        trainPerceptron(training_data, .01)
    elif exp_type.lower() == 'exp2':
        for i in range(0,num_of_features):
            weightVector.insert(i, random.random())
        bias = random.random()
        for margin in margins:
            for learning_rate in learning_rates:
                w = weightVector[:]
                bias_in_loop = bias
                if margin == 0:
                    print("----------------------------------------------------- Experimenting with Normal Perceptron where Margin = 0 and learning rate = ",learning_rate, 
                      " ---------------------------------------------------------")
                else:
                    print("----------------------------------------------------- Experimenting with Margin Perceptron where margin = ",margin," and learning rate = ",learning_rate, 
                      " ---------------------------------------------------------")
                trainMarginPerceptron(training_data, learning_rate, margin,1,0,0)
                testPerceptron(test_data,learning_rate,margin,1)
                w=[]
                bias_in_loop = 0
        print("----------------------------------------------------------------------------------------------------------------------------",
        "-----------------------------------------------------------------------------------------")
        print()
        print('Normal Perceptron Best Accuracy = ',best_accuracy_normal,' at learning rate =',best_learning_rate_normal)
        print('Margin Perceptron Best Accuracy = ',best_accuracy,' at learning rate =',best_learning_rate,' and margin =',best_margin)
        print()

        print("----------------------------------------------------- Results of Normal Perceptron with best learning rate = ",best_learning_rate_normal, 
                      " ---------------------------------------------------------")
        w = weightVector[:]
        bias_in_loop = bias
        trainMarginPerceptron(training_data, best_learning_rate_normal, 0, 1, 0,0)
        testPerceptron(test_data,best_learning_rate_normal,0, 1)
        w=[]
        bias_in_loop = 0
        print("----------------------------------------------------- Results of Margin Perceptron with best margin = ",best_margin,
              " and best learning rate = ",best_learning_rate," ---------------------------------------------------------")
        w = weightVector[:]
        bias_in_loop = bias
        trainMarginPerceptron(training_data, best_learning_rate, best_margin,1,0,0)
        testPerceptron(test_data,best_learning_rate,best_margin,1)
    elif exp_type.lower() == 'exp3':
        for i in range(0,num_of_features):
            weightVector.insert(i, random.random())
        bias = random.random()
        for epoch in epochs:
            print()
            print()
            print("---------------------------------------------------------------------------------------------- Experimenting with epoch count = ",epoch, 
                          " -----------------------------------------------------------------------------------------------------------------------------")
            #===================================================================
            # for margin in margins:
            #     for learning_rate in learning_rates:
            #===================================================================
            print("------------------------------- Experimenting without shuffle", 
                          " ------------------------------------------------")
            w = weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Normal Perceptron where Margin = 0 and learning rate = ",0.5, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0.5, 0, 1, epoch,0)
            testPerceptron(test_data,0.5,0, 1)
            w=weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Margin Perceptron where margin = ",5," and learning rate = ",0.1, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0.1, 5, 1, epoch,0)
            testPerceptron(test_data,0.1,5, 1)
            w=[]
            bias_in_loop = 0
            print("------------------------------- Experimenting with shuffle", 
                          " ------------------------------------------------")
            w = weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Normal Perceptron where Margin = 0 and learning rate = ",0.5, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0.5, 0, 1, epoch,1)
            testPerceptron(test_data,0.5,0, 1)
            w=weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Margin Perceptron where margin = ",5," and learning rate = ",0.1, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0.1, 5, 1, epoch,1)
            testPerceptron(test_data,0.1,5, 1)
            w=[]
            bias_in_loop = 0
    elif exp_type.lower() == 'exp4':
        for i in range(0,num_of_features):
            weightVector.insert(i, random.random())
        bias = random.random()
        for epoch in epochs:
            print()
            print()
            print("---------------------------------------------------------------------------------------------- Experimenting with epoch count = ",epoch, 
                          " -----------------------------------------------------------------------------------------------------------------------------")
            print("------------------------------- Experimenting without shuffle", 
                          " ------------------------------------------------")
            w = weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Aggressive Margin Perceptron where margin = ",5, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0, 5, 1, epoch,0)
            testPerceptron(test_data,0,5, 1)
            w=[]
            bias_in_loop = 0
            print("------------------------------- Experimenting with shuffle", 
                          " ------------------------------------------------")
            w = weightVector[:]
            bias_in_loop = bias
            print("----------------------------------------------------- Experimenting with Aggressive Margin Perceptron where margin = ",5, 
                          " ---------------------------------------------------------")
            trainMarginPerceptron(training_data, 0, 5, 1, epoch,1)
            testPerceptron(test_data,0,5, 1)
            w=[]
            bias_in_loop = 0