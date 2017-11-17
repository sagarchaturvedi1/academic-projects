'''
Created on Oct 2, 2016

@author: sagar
'''

import sys

if __name__ == '__main__':
    grammar_file = open(sys.argv[1], 'r')
    sentence_file = open(sys.argv[2], 'r')
    grammar_rules = grammar_file.readlines()
    sentences = sentence_file.readlines()

    for sentence in sentences:
        word_list = sentence.strip().split(" ")
        length = len(word_list)
        Matrix = [[[] for x in range(length+1)] for y in range(length+1)]

        for c in range(1,length+1):
            for rule in grammar_rules:
                rule_part = rule.strip().split('->')
                if rule_part[1].strip() == word_list[c-1].strip():
                    Matrix[c][c].append(rule_part[0].strip())
            
#        for c in range(1,length+1):
            for r in range(c-1,0,-1):
                for s in range(r+1,c+1):
                    B = Matrix[r][s-1]
                    C = Matrix[s][c]
                    for prev in B:
                        for curr in C:                               
                            for rule in grammar_rules:
                                rule_part = rule.strip().split('->')
                                if len(rule_part[1].strip().split(' ')) > 1:
                                    value1 = rule_part[1].strip().split(' ')[0].strip()
                                    value2 = rule_part[1].strip().split(' ')[1].strip()
                                    if value1 == prev and value2 == curr:
                                        Matrix[r][c].append(rule_part[0].strip())

        print 'PARSING SENTENCE:',sentence
        print 'NUMBER OF PARSES FOUND:',sum(y == 'S' for y in Matrix[1][length])
        print 'CHART:'
        for row in range(1, length+1):
            for column in range(1,length+1):
                if column >= row:
                    if len(Matrix[row][column]) == 0:
                        print '  chart['+str(row)+','+str(column)+']: -'
                    else:
                        output = ''
                        for item in Matrix[row][column]:
                            output = output + ' ' + item    
                        print '  chart['+str(row)+','+str(column)+']:',output.strip()
        
        print
        print
   
