# adventofcode 2024
# crushallhumans
# puzzle 5
# 12/5/2024

import os
import re
import sys
import math
import unittest
import socket
import hashlib
import pprint
import random
import time
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2024'
DEBUG = False
TEST_INPUT_STRING_ONE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 143
TEST_TWO_RESULT = 123


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = [[],[]]
        first = 1
        for i in l:
            if not i:
                first = 0
            else:
                if first:
                    param_set[0].append(re.split(r'\|',i))
                else:
                    param_set[1].append(re.split(',',i))
                        
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    
    before = {}
    afterr = {}
    for i in param_set[0]:
        b = i[0]
        a = i[1]
        # initialize
        if b not in before:
            before[b] = []
        if a not in afterr:
            afterr[a] = []
        # store
        if b not in afterr[a]:
            afterr[a].append(b)
        if a not in before[b]:
            before[b].append(a)

    for update in param_set[1]:
        P(update)
        bad_sequence = sequence_is_bad(update,before,afterr)

        if bad_sequence and is_two_star:
            update_reordered = reorder_update(update,before,afterr,bad_sequence)
            if update_reordered:
                P('good reorder: ', update_reordered)
                c += int(update_reordered[math.floor(len(update_reordered)/2)])
        elif not bad_sequence and not is_two_star:
            c += int(update[math.floor(len(update)/2)])

        P(bad_sequence,c)
        P('--------------------')
        P('                                                                  ')
        P('                                                                  ')

    return c

def sequence_is_bad(update,before,afterr):
    P('sequence_is_bad?',update)
    for page_idx in range(len(update)-1):
        page = update[page_idx]
        for step in range(page_idx+1,len(update)):
            if (page not in before) or (update[step] not in before[page]):
                P('bad',page,step,update[step],page in before)
                return (page,page_idx,step,update[step],page in before)

    # check last member in afterr
    P(update[len(update)-1])
    if update[len(update)-1] not in afterr:
        P('bad end', update[len(update)-1])
        return (len(update)-1,0,update[len(update)-1]) 

    return False

def reorder_update(update,before,afterr,bad_finding):
    reordered_update = update.copy()
    last_moved = False
    P(bad_finding)
    if bad_finding[4] == False:
        reordered_update.remove(bad_finding[0])
        reordered_update.append(bad_finding[0])

    P('reordered end check',reordered_update)
    not_good = sequence_is_bad(reordered_update,before,afterr)

    if not not_good:
        return reordered_update
    else:
        step = 0
        limit = 10000
        while not_good and step < (len(update)*100):
            # start swappin elements
            P('not good',not_good)
            a = not_good[0]
            b = not_good[3]
            reordered_update[not_good[1]] = b
            reordered_update[not_good[2]] = a
            not_good = sequence_is_bad(reordered_update,before,afterr)
            step += 1



    if not_good: 
        P('finally bad')
        return False
    else:
        return reordered_update


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)


def puzzle_text():
    print("""--- Day N: X ---

""")







#---------------------------------------------------------
def P(*args):
    if DEBUG:
        if len([*args]) > 1:
            pp.pprint([*args])
        else:
            pp.pprint(*args)


class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    def test_one_star(self):
        self.assertEqual(
            one_star(TEST_INPUT_STRING_ONE),
            TEST_ONE_RESULT
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(TEST_INPUT_STRING_TWO),
            TEST_TWO_RESULT
        )



if __name__ == '__main__':
    try:
        sys.argv[1]
        puzzle_text()

    except:
        DEBUG = False

        username = 'crushing'
        m = hashlib.sha256()
        hostname = socket.gethostname()
        m.update(hostname.encode('utf8'))
        if m.hexdigest() == 'ec7c98e2b47378ec88e1f9cce8d6ed91b9d616787c8a37023fd5c67cef1ff71f':
            username = 'conrad.rushing'
        print ('hostname str :',hostname)
        print ('hostname hash:', m.hexdigest())

        filename_script = os.path.basename(__file__)
        print("---------------%s--------------------"%filename_script)
        filename = filename_script.split('.')[0]
        input_set = ()
        
        with open("/Users/%s/Development/crushallhumans/adventofcode%s/inputs/%s.txt" % (username,ADVENT_YEAR,filename)) as input_file:
            input_set = reprocess_input(input_file.read())

        start = (time.time() * 1000)
        ret = one_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')

        start = (time.time() * 1000)
        ret = two_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')
