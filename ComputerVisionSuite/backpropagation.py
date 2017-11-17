'''
Created on Jan 26, 2017

@author: sagar
'''

from math import exp
import sys

def create_layer(weights,n_inputs):
    hidden_layer = []
    count = 0
    while count < len(weights)-1:
        dict = {}
        l = weights[count:count+n_inputs]
        l.append(weights[-1])
        count+=n_inputs
        dict['weights'] = l
        hidden_layer.append(dict)
    return hidden_layer
    
def create_net(layers, n_inputs, params):
    network = list()
    
    for i in range(layers):
        layer_weights = params[i]
        hidden_layer = create_layer(layer_weights, n_inputs)
        network.append(hidden_layer)    
    
    output_weights = params[-1]
    output_layer = create_layer(output_weights, n_inputs)
    network.append(output_layer)
    return network

def get_activation(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation

def sigmoid(activation):
    return 1.0 / (1.0 + exp(-activation))

def forward(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = get_activation(neuron['weights'], inputs)
            neuron['output'] = sigmoid(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

def derivative_wrt_net(output):
    return output * (1.0 - output)

def backward(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            print
            print
            for j in range(len(layer)):
                error = 0.0
                c = 0
                for neuron in network[i + 1]:
                    c+=1
                    e = neuron['weights'][j] * neuron['delta']
                    print 'Partial derivative of Error',c,' w.r.t output of hidden',str(i+1)+str(j+1),' = ',e
                    error += e
                print 'Partial derivative of Total Error w.r.t output of hidden',str(i+1)+str(j+1),' = ',error    
                errors.append(error)
                print
                print
        else:
            
            for j in range(len(layer)):
                neuron = layer[j]
                pd_error_output = neuron['output'] - expected[j]
                print 'Partial derivative of Total Error w.r.t output node',str(i+1)+str(j+1),' = ',pd_error_output
                errors.append(pd_error_output)
                print
                
        for j in range(len(layer)):
            neuron = layer[j]
            pd_output_net = derivative_wrt_net(neuron['output'])
            print 'Partial derivative of node',str(i+1)+str(j+1),' w.r.t Net',str(i+1)+str(j+1),' = ',pd_output_net
            neuron['delta'] = errors[j] * pd_output_net
            print 'Delta of node',str(i+1)+str(j+1),' = ',neuron['delta']
            print
            

def update(network, row, l_rate):
    count = 0
    for i in range(len(network)):
        inputs = row
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                count+=1
                print 'Partial derivative of net of next node w.r.t weight',count,' = ',inputs[j]
                pd_error_weight = neuron['delta'] * inputs[j]
                print 'Partial derivative of Total Error w.r.t weight',count,' = ',pd_error_weight
                neuron['weights'][j] -= l_rate * pd_error_weight
                print
                print '**************************************************** Updated weight',count,' = ',neuron['weights'][j],'**************'
                print
            neuron['weights'][-1] -= l_rate * neuron['delta']
            print '**************************************************** Updated bias',i+1,' = ',neuron['weights'][-1],'**************'
            print

# Train a network for a fixed number of epochs
def train(network, train, l_rate, n_epoch, n_inputs):
    for epoch in range(n_epoch):
        for row in train:
            expected = row[n_inputs:n_inputs+n_inputs]
            row = row[0:n_inputs]
            forward(network, row)
            print
            print 'Forward pass complete. network looks like'
            print network
            print
            print 'Backward pass starting ----'
            print
            backward(network, expected)
            update(network, row, l_rate)
        print
        print 'learning rate used = ',l_rate
        print

# Test training backprop algorithm

layers = int(sys.argv[1])
n_inputs = int(sys.argv[2])
paramfile = open(sys.argv[3]).readlines()
datafile = open(sys.argv[4]).readlines()

dataset = []
params = []
for line in datafile:
    dataset.append(map(float, line.strip().split(',')))
for line in paramfile:
    params.append(map(float, line.strip().split(',')))

#dataset = map(float, dataset)
#params = map(float, params)


network = create_net(layers, n_inputs, params)
print 'Netwrok initialized. It looks like - '
print network
print
train(network, dataset, 0.5, 1, n_inputs)


