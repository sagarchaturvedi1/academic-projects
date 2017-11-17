'''
Created on Jan 29, 2017

@author: sagar
'''

from numpy import shape
import numpy as np
import pandas as pd
import sys
train_file_name = sys.argv[1].strip()
test_file_name = sys.argv[2].strip()
ftype = sys.argv[3].strip()
uniq_words = []
uniq_pos = []
uniq_label = []
feature_dict = {}
pos_dict = {}

def write_to_file(input,fname):
    with open(fname,'wb') as f:
        for row in input:
            l = sorted(row[1:len(row)], key=lambda x: float(x))
            string = ":1 ".join(l[i] for i in xrange(1,len(l)))
            f.write(l[0]+' '+string+':1\n')

def write_f(train_w,test_w):
    write_to_file(train_w, train_file_name+'.'+ftype)
    write_to_file(test_w, test_file_name+'.'+ftype)
        
def get_list(data):
    a_list = []
    # Handle blank lines
    for line in data:
        a = line.strip().split()
        if not a:
            a = ['','','']
        a_list.append(a)
    return a_list

def get_test_pos(pos,position):
    if pos.strip()=='':
        pos = get_test_pos_position(pos,position)
    elif pos not in uniq_pos:
        pos = 'UNKPOS'
    return pos

def get_test_pos_position(pos,position):
    if position=='next':
        pos = 'OMEGAPOS'
    else:
        pos = 'PHIPOS'
    return pos

def get_test_word(word,position):
    if word.strip()=='':
        word = get_test_word_position(word,position)
    elif word not in uniq_words:
        word = 'UNKWORD'
    return word

def get_test_word_position(word,position):
    if position=='next':
        word = 'OMEGA'
    else:
        word = 'PHI'
    return word

def main():
    global uniq_words,uniq_pos,uniq_label,feature_dict,pos_dict
    training_data = open(train_file_name, 'r').readlines()
    test_data = open(test_file_name, 'r').readlines()
    
    train_list = get_list(training_data)
    test_list = get_list(test_data)
    
    #===========================================================================
    # train_list = [map(str, line.strip().split()) for line in training_data]
    # test_list = [map(str, line.strip().split()) for line in test_data]
    #===========================================================================
     
    #Create NP arrays
    train_array = np.asarray(train_list)
    test_array = np.asarray(test_list)

    print shape(train_array)
    print shape(test_array)
  
    uniq_words = np.unique(train_array[:,2])
    uniq_pos = np.unique(train_array[:,1])
    #uniq_label = np.unique(train_array[:,0])

    #label_dict = {}
    
    label_dict = {
    'O' : 0,
    'B-PER' : '1',
    'I-PER' : '2',
    'B-LOC' : '3',
    'I-LOC' : '4',
    'B-ORG' : '5',
    'I-ORG' : '6'
    }

    #Create Unique word dictionary
    for i in xrange(len(uniq_words)):
        if uniq_words[i] != '':
            feature_dict['curr-'+uniq_words[i]] = (3*i)+1
            feature_dict['prev-'+uniq_words[i]] = (3*i)+2
            feature_dict['next-'+uniq_words[i]] = (3*i)+3
        
    #feature_dict['curr-PHI'] = len(feature_dict)+1
    #feature_dict['curr-OMEGA'] = len(feature_dict)+1
    feature_dict['curr-UNKWORD'] = len(feature_dict)+1
    
    feature_dict['prev-PHI'] = len(feature_dict)+1
    #feature_dict['prev-OMEGA'] = len(feature_dict)+1
    feature_dict['prev-UNKWORD'] = len(feature_dict)+1
    
    #feature_dict['next-PHI'] = len(feature_dict)+1
    feature_dict['next-OMEGA'] = len(feature_dict)+1
    feature_dict['next-UNKWORD'] = len(feature_dict)+1
    
    feature_dict['capitalized'] = len(feature_dict)+1

    #Create Unique pos dictionary
    for i in xrange(len(uniq_pos)):
        if uniq_pos[i] != '':
            #pos_dict['curr-'+uniq_pos[i]] = len(feature_dict)+len(pos_dict)+1
            pos_dict['prev-'+uniq_pos[i]] = len(feature_dict)+len(pos_dict)+1
            pos_dict['next-'+uniq_pos[i]] = len(feature_dict)+len(pos_dict)+1     
    
    
    #pos_dict['curr-PHIPOS'] = len(feature_dict)+len(pos_dict)+1
    #pos_dict['curr-OMEGAPOS'] = len(feature_dict)+len(pos_dict)+1
    #pos_dict['curr-UNKPOS'] = len(feature_dict)+len(pos_dict)+1
    
    pos_dict['prev-PHIPOS'] = len(feature_dict)+len(pos_dict)+1
    #pos_dict['prev-OMEGAPOS'] = len(feature_dict)+len(pos_dict)+1
    pos_dict['prev-UNKPOS'] = len(feature_dict)+len(pos_dict)+1
    
    #pos_dict['next-PHIPOS'] = len(feature_dict)+len(pos_dict)+1
    pos_dict['next-OMEGAPOS'] = len(feature_dict)+len(pos_dict)+1
    pos_dict['next-UNKPOS'] = len(feature_dict)+len(pos_dict)+1

 #==============================================================================
 #    #Create word features data frame
 #    col_names = np.insert(uniq_words, 0,'label')
 #    word_train = pd.DataFrame(index=train_array[:,2], columns=col_names,dtype=str).fillna('0')
 #    word_test = pd.DataFrame(index=test_array[:,2], columns=col_names,dtype=str).fillna('0')
 # 
 #    for x in train_list:
 #        word_train.set_value(x[2], x[2], 1)
 #        word_train.set_value(x[2], 'label', x[0])
 #     
 #    for x in test_list:
 #        word_test.set_value(x[2], x[2], 1)
 #        word_test.set_value(x[2], 'label', x[0])
 #         
 #    print word_train
 #    #print word_test
 #==============================================================================

    #create train and test word features
    train_w = [[]]
    test_w = [[]]
    for i in train_array:
        if i[2] != '':
            row = [i[2]]
            row.append(str(label_dict[i[0]]))
            row.append(str(feature_dict['curr-'+i[2]]))
            train_w.append(row)
        
    for i in test_array:
        if i[2] != '':
            row = [i[2]]
            row.append(str(label_dict[i[0]]))
            if i[2] in uniq_words:
                row.append(str(feature_dict['curr-'+i[2]]))
            else:
                row.append(str(feature_dict['curr-UNKWORD']))
            test_w.append(row)           
    
    train_w = filter(None, train_w)
    test_w = filter(None, test_w)
    
    if ftype.lower() == 'word':
        write_f(train_w, test_w)
        return
    
    #create train and test wordcap features
    for i in train_w:
        if i[0][0].isupper():
                i.append(str(feature_dict['capitalized']))
    for i in test_w:
        if i[0][0].isupper():
                i.append(str(feature_dict['capitalized']))
                
    if ftype.lower() == 'wordcap':
        write_f(train_w, test_w)
        return
    
    #create train and test poscon features
    if ftype.lower() in ['poscon','bothcon'] :
        count = 0
        for ind in xrange(len(train_array)):
            i = train_array[ind]
            if i[2] != '':
                word_index = ind - count
                prev_pos=''
                next_pos=''
                if ind == 0 or train_array[ind-1][1].strip()=='':
                    prev_pos = str(pos_dict['prev-PHIPOS'])
                    next_pos = str(pos_dict['next-'+get_test_pos(train_array[ind+1][1].strip(),'next')])
                elif ind == len(train_array)-1 or train_array[ind+1][1].strip()=='':
                    prev_pos = str(pos_dict['prev-'+get_test_pos(train_array[ind-1][1].strip(),'prev')])
                    next_pos = str(pos_dict['next-OMEGAPOS'])
                else:
                    prev_pos = str(pos_dict['prev-'+get_test_pos(train_array[ind-1][1].strip(),'prev')])
                    next_pos = str(pos_dict['next-'+get_test_pos(train_array[ind+1][1].strip(),'next')])
                train_w[word_index].append(prev_pos)
                train_w[word_index].append(next_pos)
            else:
                count+=1
        
        count = 0              
        for ind in xrange(len(test_array)):
            i = test_array[ind]
            if i[2] != '':
                word_index = ind - count
                prev_pos=''
                next_pos=''
                if ind == 0 or test_array[ind-1][1].strip()=='':
                    prev_pos = str(pos_dict['prev-PHIPOS'])
                    next_pos = str(pos_dict['next-'+get_test_pos(test_array[ind+1][1].strip(),'next')])
                elif ind == len(test_array)-1 or test_array[ind+1][1].strip()=='':
                    prev_pos = str(pos_dict['prev-'+get_test_pos(test_array[ind-1][1].strip(),'prev')])
                    next_pos = str(pos_dict['next-OMEGAPOS'])
                else:
                    prev_pos = str(pos_dict['prev-'+get_test_pos(test_array[ind-1][1].strip(),'prev')])
                    next_pos = str(pos_dict['next-'+get_test_pos(test_array[ind+1][1].strip(),'next')])
                test_w[word_index].append(prev_pos)
                test_w[word_index].append(next_pos)
            else:
                count+=1
    
    if ftype.lower() == 'poscon':
        write_f(train_w, test_w)
        return
    
    
    
    #create train and test lexcon features
    if ftype.lower() in ['lexcon','bothcon'] :
        count = 0
        for ind in xrange(len(train_array)):
            i = train_array[ind]
            if i[2] != '':
                word_index = ind - count
                prev_word=''
                next_word=''
                if ind == 0 or train_array[ind-1][2].strip()=='':
                    prev_word = str(feature_dict['prev-PHI'])
                    next_word = str(feature_dict['next-'+get_test_word(train_array[ind+1][2].strip(),'next')])
                elif ind == len(train_array)-1 or train_array[ind+1][2].strip()=='':
                    prev_word = str(feature_dict['prev-'+get_test_word(train_array[ind-1][2].strip(),'prev')])
                    next_word = str(feature_dict['next-OMEGA'])
                else:
                    prev_word = str(feature_dict['prev-'+get_test_word(train_array[ind-1][2].strip(),'prev')])
                    next_word = str(feature_dict['next-'+get_test_word(train_array[ind+1][2].strip(),'next')])
                train_w[word_index].append(prev_word)
                train_w[word_index].append(next_word)
            else:
                count+=1
        
        count = 0              
        for ind in xrange(len(test_array)):
            i = test_array[ind]
            if i[2] != '':
                word_index = ind - count
                prev_word=''
                next_word=''
                if ind == 0 or test_array[ind-1][2].strip()=='':
                    prev_word = str(feature_dict['prev-PHI'])
                    next_word = str(feature_dict['next-'+get_test_word(test_array[ind+1][2].strip(),'next')])
                elif ind == len(test_array)-1 or test_array[ind+1][2].strip()=='':
                    prev_word = str(feature_dict['prev-'+get_test_word(test_array[ind-1][2].strip(),'prev')])
                    next_word = str(feature_dict['next-OMEGA'])
                else:
                    prev_word = str(feature_dict['prev-'+get_test_word(test_array[ind-1][2].strip(),'prev')])
                    next_word = str(feature_dict['next-'+get_test_word(test_array[ind+1][2].strip(),'next')])
                test_w[word_index].append(prev_word)
                test_w[word_index].append(next_word)
            else:
                count+=1
    
    write_f(train_w, test_w)
    
if __name__ == '__main__':
    main()