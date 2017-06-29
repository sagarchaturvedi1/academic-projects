'''
Created on Nov 8, 2016

@author: sagar
'''

from IPython.display import Image
import csv
import random
import subprocess
import pydotplus
import os
from sklearn import svm
from sklearn import tree, preprocessing
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm.classes import LinearSVC
from graphviz.dot import Dot
from IPython.core.display import display


### Read Train and test Data ####
train_d = {}

# Read Bird Dataset Features ########
with open('image_attribute_labels_50.txt', mode='r') as infile:
    reader = csv.reader(infile,delimiter=" ")
    for rows in reader:
        if rows[0] in train_d:
            train_d[rows[0]].append(rows[2])
        else:
            A = [rows[2]]
            train_d[rows[0]] = A

### Read Tensorflow features ###

#===============================================================================
# with open('TF_features.csv', mode='r') as infile:
#     reader = csv.reader(infile,delimiter=",")
#     count = 0
#     for rows in reader:
#         count += 1
#         train_d[str(count)] = rows
# 
# print 'length of featureset =',len(train_d['1'])
#===============================================================================
		
with open('image_class_labels_50.txt', mode='r') as file1:
    reader1 = csv.reader(file1,delimiter=" ")
    for rows in reader1:
        train_d[rows[0]].append(rows[1])

keys =  list(train_d.keys())
random.shuffle(keys)

dict1 = {}
for key in keys:
    dict1[key] = train_d[key]
 
train_data = {}
test_data = {}
c = 0
n = int(.8 * len(dict1))
for k,v in dict1.items():
    if c < n:
        train_data[k] = v
    else:
        test_data[k] = v
    c += 1

X = []
Y = []
for key in train_data.keys():
    X.append(train_data[key][0:-1])
    Y.append(train_data[key][-1])

A = []
B = []
for key in test_data.keys():
    A.append(test_data[key][0:-1])
    B.append(test_data[key][-1])
    
# PCA #
#===============================================================================
# pca = PCA()  
# pca.fit_transform(X)
# 
# print(pca.explained_variance_ratio_)
# 
# pca.n_components = 158
# X_reduced = pca.fit_transform(X)
# print(X_reduced.shape)
#===============================================================================

#===============================================================================
# print(pca.components_)
# print(pca.mean_)
# print(pca.get_covariance())
# print(pca.get_precision())
#===============================================================================

## Decision Tree ## 

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
scores = cross_val_score(clf, X, Y, cv=5)
 
print 'CV = ',scores

#print(clf.tree_.compute_feature_importances())
   
result = clf.predict(A)
print 'Test Accuracy = ',accuracy_score(result, B)

print 'Tree Actual Depth = ',clf.tree_.max_depth

with open("birds.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f,max_depth=5)
 

subprocess.call(['dot', '-Tpng', 'birds.dot', '-o' 'birds.png'])

#===============================================================================
# dot_data = tree.export_graphviz(clf,out_file="birds.dot")
# graph = pydotplus.graph_from_dot_file("birds.dot")
# display(Image(graph.create_pdf())) 
#===============================================================================

#Label Binarizer
#===============================================================================
# lb = preprocessing.LabelBinarizer()
# Y1 = lb.fit_transform(Y)
# 
# olf = OneVsRestClassifier(LinearSVC()).fit(X, Y1)
# scores1 = cross_val_score(olf, X, Y1, cv=10)
# print(scores1)
#===============================================================================

### SVM One vs Rest ###
#===============================================================================
# clf = OneVsRestClassifier(LinearSVC(C=5, tol=1e-10,class_weight='balanced'))
# clf = clf.fit(X, Y)
# #===============================================================================
# # scores = cross_val_score(clf, X, Y, cv=10)
# # print scores
# #===============================================================================
# result = clf.predict(A)
# print(accuracy_score(result, B))
#===============================================================================

## SVM non linear #####
#===============================================================================
# C_values = [.5,1,2,5,10,100]
# gamma_values = [.1,.01,.001,.0001]
# for gamma in gamma_values:
#     for c in C_values:
#         print 'learning_rate =',gamma,',C =',c 
#         clf = svm.SVC(C=c, tol=1e-10, cache_size=600, kernel='rbf', gamma=gamma, 
#               class_weight='balanced')
#         clf = clf.fit(X, Y)
#         scores = cross_val_score(clf, X, Y, cv=5)
#         print scores
#         print 'Max cross validation accuracy =',max(scores)
#         result = clf.predict(A)
#         print 'Accuracy on test set =',accuracy_score(result, B)
#         print
#         print
#===============================================================================






