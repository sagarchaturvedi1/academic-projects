'''
Created on Feb 28, 2017

@author: Sagar
'''


import pandas as pd
import numpy as np
import math
import sys
from pandas import DataFrame




## Get the MI score
def get_sim(triple_rules, path, word, slot):
    X = triple_rules[(triple_rules['path'] == path) & 
                     (triple_rules['slot' + slot] == word)]
    numerator = X.size * triple_rules.size
    Y = triple_rules[triple_rules['path'] == path]
    Z = triple_rules[triple_rules['slot' + slot] == word]
    denominator = Y.size * Z.size
    if numerator == 0 or denominator == 0 or math.log2(numerator/denominator) < 0:
        return 0
    mi = math.log2(numerator/denominator)
    return mi

## Main function
def main():
    stopword_list = ['>comma', '>squote', '>period', '>minus', '>rparen', '>lparen', '>ampersand',
                 'is', 'are', 'and', 'or', 'be', 'was', 'were', 'said', 'have', 'has', 'had']
    table_columns=['slotx', 'path', 'sloty']
    file_name = sys.argv[1]
    test_file = sys.argv[2]
    
    triple_rules = DataFrame(columns=table_columns)
    corpus_file = open(file_name)
    corpus_data = [[word.strip() for word in line.split(':')] for line in corpus_file]
    for i in range(0,len(corpus_data)):
        rows = corpus_data[i]
        current_type = rows[0]
        current_phrase = rows[1]
        if current_type == 'NP':
            j = i + 1
            path_phrase = ''
            while(True):
                next_type = corpus_data[j][0]
                next_phrase = corpus_data[j][1]
                if next_type == 'NP' or next_phrase == '<EOS':
                    break
                path_phrase = path_phrase + " " + next_phrase
                j = j + 1
            
            path_phrase = path_phrase.strip()
            if (path_phrase.lower() in stopword_list and 
                len(path_phrase.split()) == 1) or path_phrase == '' or next_phrase == '<EOS' :
                continue
            else:
                triple_rules = triple_rules.append({'slotx':current_phrase.split()[-1].lower(), 'path':path_phrase.lower(), 
                                                    'sloty':next_phrase.split()[-1].lower()}, ignore_index=True)
                
    old_no_of_rows = triple_rules.shape[0]
    count = triple_rules['path'].value_counts()
    old_unique_paths = count.size
    to_remove = count[count < int(sys.argv[3])].index
    triple_rules = triple_rules[~triple_rules['path'].isin(to_remove)]
    new_rows = triple_rules.shape[0]
    new_unique_paths = triple_rules['path'].value_counts().size
    print('Found', old_unique_paths, 'distinct paths,', new_unique_paths, 'after minfreq filtering.')
    print('Found', old_no_of_rows, 'path instances,', new_rows, 'after minfreq filtering.' )
    print()
    
    
    test_file = open(test_file)
    vc = triple_rules['path'].value_counts()
    distinct_p = vc.index
    for line in test_file:
        line = line.strip().lower()
        print('MOST SIMILAR RULES FOR:', line)
        rules = triple_rules[triple_rules['path'] == line]
        
        if rules.size == 0:
            print("This phrase is not in the triple database.")
            continue
        
        x = rules['slotx'].value_counts().index
        y = rules['sloty'].value_counts().index
                
        output = DataFrame(columns={'path', 'score'})
        for path in distinct_p:
            paths = triple_rules[triple_rules['path'] == path]
            xp = paths['slotx'].value_counts()
            xi = triple_rules[(triple_rules['path'] == path) & 
                              (triple_rules['slotx'].isin(x))]['slotx'].value_counts()
            yp = paths['sloty'].value_counts()
            yi = triple_rules[(triple_rules['path'] == path) & 
                              (triple_rules['sloty'].isin(y))]['sloty'].value_counts()
            
            if xi.size == 0 or yi.size == 0:
                continue  
            numerator = 0
            for w in xi.index:
                numerator = numerator + (get_sim(triple_rules, line, w, 'x') + 
                              get_sim(triple_rules, path, w, 'x'))
            denominator = 0
            for w in x:
                denominator = denominator + get_sim(triple_rules, line, w, 'x')
            for w in xp.index:
                denominator = denominator + get_sim(triple_rules, path, w, 'x')
            xs = numerator/denominator
            numerator = 0
            for w in yi.index:
                numerator = numerator + (get_sim(triple_rules, line, w, 'y') + 
                              get_sim(triple_rules, path, w, 'y'))
            denominator = 0
            for w in y:
                denominator = denominator + get_sim(triple_rules, line, w, 'y')
            for w in yp.index:
                denominator = denominator + get_sim(triple_rules, path, w, 'y')
            ys = numerator/denominator
            total_sim = math.sqrt(xs * ys)
            output = output.append({'path' : path, 'score' : total_sim}, ignore_index=True)  
        
        output = output.sort_values(by='score', ascending=False).reset_index(drop=True)
        
        if output.size > 5:
            output = output[output['score'] >= output.ix[4, 'score']]
        
        for index, row in output.iterrows():
            print(str(index+1)+'.',row['path'],'\t',row['score'])
        
        
        print()
    
if __name__ == '__main__':
    main()