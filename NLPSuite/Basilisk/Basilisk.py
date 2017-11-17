'''
Created on Oct 31, 2016

@author: sagar
'''

from sys import argv
from math import log

contexts_file = open(argv[2], 'r')
seed_word_file = open(argv[1], 'r')
lex_set = set()
patterns = {}
seed_word_list = []

for seed_word in seed_word_file:
    lex_set.add(seed_word.strip("\n").lower())
    seed_word_list.append(seed_word.strip("\n").lower())

print()
print("Seed Words:", ' '.join(seed_word_list))

for row in contexts_file:
    pattern_list = row.strip("\n").split()
    index_of_star = pattern_list.index('*')
    listed_pattern = pattern_list[index_of_star + 1]
    head_noun = pattern_list[index_of_star - 1]
    if listed_pattern not in patterns:
        patterns[listed_pattern] = [set(), set(), 0.0]
    patterns[listed_pattern][0].add(head_noun.lower())
print("Unique patterns:", len(patterns))

for i in range(1,6):
    group_of_patterns =[]
    group_of_candidates = []
    candidate_dict = {}
    for pat in patterns:    
        patterns[pat][1].update(patterns[pat][0].intersection(lex_set))
        patterns[pat][2] = ((len(patterns[pat][1])/len(patterns[pat][0]))* log(len(patterns[pat][0]),2))

    reversed_pattern = {}       
    for k, v in patterns.items():
        if v[2] not in reversed_pattern:
            reversed_pattern[v[2]] = set()
        reversed_pattern[v[2]].update([k])

    rlogf_score = sorted(reversed_pattern.keys(),reverse = True)[:]
    i_value = 0
    c = 1
    while c <= 10:
        if len(rlogf_score) > i_value and rlogf_score[i_value] != 0:
            list1 = sorted(reversed_pattern[rlogf_score[i_value]])
            for pat in list1:
                group_of_patterns.append(pat + "  (" + str("%.3f"%(rlogf_score[i_value])) + ")")
                c = c+1
                for k in patterns[pat][0]:
                    if k not in candidate_dict:
                        candidate_dict[k] = [set(), 0.0]
        else:
            break                   
        i_value = i_value + 1


    for pat in patterns:
        for cand in candidate_dict:
            if cand in patterns[pat][0]:
                candidate_dict[cand][0].update([pat])

    for k, v in candidate_dict.items():
        score = 0.0
        f = 0.0
        for pat in v[0]:
            exp = patterns[pat]
            f = len((exp[0].intersection(lex_set)).difference(k))
            score = score + log((f + 1), 2)
        candidate_dict[k][1] = score/len(candidate_dict[k][0])
     
    reverse_cand_dict = {}

    for k, v in candidate_dict.items():
        if v[1] not in reverse_cand_dict:
            reverse_cand_dict[v[1]] = set()
        reverse_cand_dict[v[1]].update([k])

    cand_score = sorted(reverse_cand_dict.keys(), reverse = True)[:]
    index_value = 0
    ctr = 1
    while ctr <= 5:
        if len(cand_score) <= index_value:
            break
        else:
            list2 = sorted(reverse_cand_dict[cand_score[index_value]])
            for cand in list2:
                if cand not in lex_set:
                    lex_set.update([cand])
                    group_of_candidates.append(cand + '  (%.3f)'%(cand_score[index_value]))
                    ctr = ctr+1
        index_value = index_value+1

    print()
    print("ITERATION", i)

    print()
    print("PATTERN POOL")
    number = 1
    for pat in group_of_patterns:
        print(str(number)+".", pat)
        number += 1

    print()
    print("NEW WORDS")
    for c in group_of_candidates:
        print(c)