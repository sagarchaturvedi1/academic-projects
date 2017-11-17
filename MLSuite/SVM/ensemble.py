
###
# for changing the option being run change option argument in function fix_missing_in_data(c_data, option=2) to 1,2 or 3
#
#

from math import *
from random import shuffle
from random import sample
from random import choice
import os
import sys
import numpy as np

attributes = {}
for i in range(0,256):
    if sys.argv[4].strip() == 'continuous':
        attributes[i+1] = [1,2,3,4,5,6,7,8,9,10]
    else:
        attributes[i+1] = [0, 1]

'''attributes = { 1: ['b', 'c', 'x', 'f', 'k', 's'],
               2: ['f', 'g', 'y', 's'],
               3: ['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'],
               4: ['t', 'f'],
               5: ['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'],
               6: ['a', 'd', 'f', 'n'],
               7: ['c', 'w', 'd'],
               8: ['b', 'n'],
               9: ['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'],
               10: ['e', 't'],
               11: ['b', 'c', 'u', 'e', 'z', 'r', '?'], #removed ?
               12: ['f', 'y', 'k', 's'],
               13: ['f', 'y', 'k', 's'],
               14: ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
               15: ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
               16: ['p', 'u'],
               17: ['n', 'o', 'w', 'y'],
               18: ['n', 'o', 't'],
               19: ['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'],
               20: ['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'],
               21: ['a', 'c', 'n', 's', 'v', 'y'],
               22: ['g', 'l', 'm', 'p', 'u', 'w', 'd']
}

label = ['e', 'p']
#label = [1, -1]

'''



def std_dev(l):
    m = (sum(l) + 0.0) / len(l)
    ssq = 0.0
    for c in l:
        ssq += (c - m)**2
    return sqrt(ssq/len(l))

def read_from_file(filename):
    f = open(filename, 'r')
    content_list = []
    for line in f.readlines():
        content_list.append(line.strip('\n').split(','))
    return content_list





def fix_missing_in_data(c_data, option=2):
    """Fixes the missing data according to the 3 options"""
    co = 0
    for row in c_data:
       lab = row[-1]
       missing = [i for i, x in enumerate(row) if x == '?']
       for ind in missing:
           atrr = attributes[ind+1]
           count = [0] * len(atrr)
           if option == 1:
                for r in c_data:
                    if r[ind] != '?':
                       count[atrr.index(r[ind])] += 1
                row[ind] = atrr[count.index(max(count))]
           if option == 2:
                for r in c_data:
                    if r[ind] != '?' and lab == r[-1]:
                        co += 1
                        count[atrr.index(r[ind])] += 1
                row[ind] = atrr[count.index(max(count))]
           if option == 3:
               return c_data
    return c_data


def count_attribute_numbers(number, c_list):
    """Counts the number of attr_val of each attribute in dataset"""
    total_count = [0, 0, 0]
    labels = attributes[number]
    counts = dict((l, [0, 0, 0]) for l in labels)
    for line in c_list:
        total_count[0] += 1
        counts[line[number-1]][0] += 1
        if line[-1] == -1:                    
            counts[line[number-1]][1] += 1
            total_count[1] += 1
        else:
            counts[line[number-1]][2] += 1
            total_count[2] += 1

    return counts, total_count

def calculate_log(p1, p2, total):
    if total == 0:
        return 0.0
    prob1 = p1/(total + 0.0)
    prob2 = p2/(total + 0.0)
    en = 0.0
    if prob1 != 0.0:
        en += -1 * prob1 * log(prob1, 2)
    if prob2 != 0.0:
        en += -1 * prob2 * log(prob2, 2)
    return en

def gen_subset_of_content(c_list, attr_val, value):
    subset = []

    for i in range(len(c_list)):
        if c_list[i][attr_val - 1] == value:
            subset.append(c_list[i])
    return subset


def calculate_entropy(attribute_count, total_count):
    entropy = 0.0
    for key in attribute_count:
        entropy += ((attribute_count[key][0] + 0.0) / total_count[0]) * calculate_log(attribute_count[key][1], attribute_count[key][2], attribute_count[key][0])

    cal_en = calculate_log(total_count[1], total_count[2], total_count[0])

    return cal_en - entropy


def find_max_gain(attr_to_consider, c_list):
    k = int(log(len(attr_to_consider),2))
    IGs = []
    if len(attr_to_consider) >= k:
        attr_to_consider = sample(attr_to_consider, k)
    for attr in attr_to_consider:
        attribute_count, total_count = count_attribute_numbers(attr, c_list)
        IGs.append(calculate_entropy(attribute_count, total_count))
    return max(IGs), attr_to_consider[IGs.index(max(IGs))]


class Node():
    def __init__(self, attribute_split, depth=0):
        self.value = attribute_split
        self.children = []
        self.attr_val = []
        self.depth = depth

    def __str__(self):
        return str(self.value)


def calculate_max_classified(s):
    c_p = 0
    c_e = 0
    for line in s:
        if line[-1] == -1:   ###negetive -1 'e'####
            c_e += 1
        else:
            c_p += 1
    if c_p >= c_e:
        return 1      ### return positive####
    else:
        return -1     #### return negetive####


### GLOBAL VARIABLE TO KEEP TRACK OF CURRENT DEPTH ####
depths = 0


def ID3(S, attribute, depth=0, limit=0, limitOn=False):
    global depths
       
    if not S:
        return
    
    if depths <= depth:
        depths = depth
    
        
    if limitOn == True:
       if limit == (depth):
           return Node(calculate_max_classified(S), depth = depth)
    
    
    if not attribute:
        return
    
    lab = S[0][-1]
    all_same = True
    for line in S[1:]:
       if line[-1] != lab:
           all_same = False
           #break
    if all_same:
        return Node(lab, depth=depth)

    
    num, attr = find_max_gain (attribute, S)
    root = Node(attr)
    values = attributes[attr]
    attribute_copy = attribute[:]
    attribute_copy.remove(attr)
    for value in values:
        root.attr_val.append(value)
        s = gen_subset_of_content(S, attr, value)
        if s == None:
            root.children.append(Node(calculate_max_classified(S)))
        else:
            ro= ID3(s, attribute_copy, depth+1, limit, limitOn)
            root.children.append(ro)
    return root


def print_tree(n):
    if n == None:
        return
    
    if n.value == 1 or n.value == -1:    
        return 
    
    if not n.children:
        return
    i = 0
    for child in n.children:
        print (n, str(n.attr_val[i]),  child)
        i += 1
        print_tree(child)



def check_example(example, root, gtruth):
    if root == None:
         return 
    if root.value == 1 or root.value == -1:             
        if root.value == gtruth:
            return True
        else:
            return False
    
    if root.children[root.attr_val.index(example[root.value - 1])] is None:
        return False
    l = root.children[root.attr_val.index(example[root.value - 1])].value
    
    
    if l == None:
        return False
    else:
        m = root.children[root.attr_val.index(example[root.value - 1])]
        if isinstance(m, Node):
            return check_example(example, m, gtruth)
        else:
            if m == gtruth:
                return True
            else:
                return False    

def get_output(example, root):
    if root == None:
        return 
    if root.value == 1 or root.value == -1:             
        return root.value
    
    if root.children[root.attr_val.index(example[root.value - 1])] is None:
        return choice([1, -1])  
    l = root.children[root.attr_val.index(example[root.value - 1])].value
    
    
    if l == None:
        return choice([1, -1]) # return False
    else:
        m = root.children[root.attr_val.index(example[root.value - 1])]
        if isinstance(m, Node):
            return get_output(example, m)
        else:
            return m  



def test_accuracy(content_test, root):
    total = 0
    correct = 0
    for example in content_test:
        if check_example(example, root, example[-1]):
            correct += 1
        total +=  1
    return (correct + 0.0 ) * 100.0 / total



def check_train_and_test_accuracy(root, train_data, test_data, dep):
    return test_accuracy(train_data, root), test_accuracy(test_data, root) 


def read_file(filename,feature_type):
    """ reads the file and return data"""
    f = open(filename)
    data = []
    for line in f.readlines():
        line = line.strip("\n").strip(" ").split(" ")
        int_line = []
        for val in line:
            int_line.append(float(val))
        data.append(int_line)
    if feature_type == 'continuous':
        data = split_features(data)
    return data
    
def read_label_file(filename):
    """ reads the file and return data"""
    f = open(filename)
    data = []
    for line in f.readlines():
        line = line.strip("\n")
        data.append(int(line))
    return data    

def split_features(data):
    data = np.asarray(data)
    digitized = data[:]
    for col in np.arange(len(data[0])):
        min_value = data[:,col].min()
        max_value = data[:,col].max()
        bucket = np.linspace(min_value, max_value, 10)
        digitized[:,col] = np.digitize(data[:,col], bucket)
    return digitized.tolist()

train_d = read_file(sys.argv[1].strip(),sys.argv[4].strip())
train_l = read_label_file(sys.argv[1].strip().replace('.data','.labels'))

test_d = read_file(sys.argv[2].strip(),sys.argv[4].strip())
test_l = read_label_file(sys.argv[2].strip().replace('.data','.labels'))



train_data = []
test_data = []
i = 0
for i in range(len(train_d)):
     l = train_d[i]
     l.append(train_l[i])
     train_data.append(l)
    
for i in range(len(test_d)):
     l = test_d[i]
     l.append(test_l[i])
     test_data.append(l)


root = ID3(train_data, list(range(1,257)))


def return_only_m_samples(data, m):
     return sample(data, m)
     

    
def train_n_trees(train_data, n, m):
    sset = sample(train_data, m)
    trees = []
    for i in range(n):
        root = ID3(sset, list(range(1,257)))
        trees.append(root)
    return trees


roots = train_n_trees(train_data, int(sys.argv[3].strip()), 500)

def prepare_output(data, roots):
    outputs = []
    labels = []
    for example in data:
        out = []
        for root in roots:
            out.append(get_output(example, root))
        labels.append(example[-1])   
        outputs.append(out)
    return outputs, labels

def write_file(data,file_name):
    with open(file_name, mode='w+', encoding='utf-8') as myfile:
        for lines in data:
            myfile.write(' '.join(str(lines).replace("[", "").replace("]", "")).replace("- 1", "-1").replace(" ,   ", " "))
            myfile.write('\n')

tr_data, tr_l = prepare_output(train_data, roots)
te_data, te_l = prepare_output(test_data, roots)

write_file(tr_data, 'train.data')
write_file(tr_l, 'train.labels')
write_file(te_data, 'test.data')
write_file(te_l, 'test.labels')

