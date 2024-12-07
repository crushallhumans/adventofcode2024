# adventofcode 2024
# crushallhumans
# puzzle 7
# 12/7/2024

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
from itertools import product
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2024'
DEBUG = False
TEST_INPUT_STRING_ONE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 3749
TEST_TWO_RESULT = 11387


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [re.split(r': ' ,input_line.strip()) for input_line in param_set.splitlines()]
        param_set = []
        for i in l:
            param_set.append([
                int(i[0]),
                [int(j) for j in re.split(r' ',i[1])]
            ])
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    d = 1
    limit = len(param_set)
    P(0,'/',limit,force=True)
    for i in param_set:

        P(d,'/',limit,end='\r',force=True)
        s = 0
        test_product = i[0]
        test_list = i[1]

        # 0 == add
        # 1 == multiply
        operator_sets = list(product([0, 1], repeat=len(test_list)-1))
        if is_two_star:
            # 2 == catenate
            operator_sets = list(product([0, 1, 2], repeat=len(test_list)-1))

        P('test: ',test_product,test_list)
        P('ops: ',operator_sets)

        for operators in operator_sets:
            P(operators)
            s = int(test_list[0])
            for op_idx in range(len(operators)):
                op = operators[op_idx]
                P('op',op)
                if op == 2:
                    s = caten_cached(s,test_list[op_idx+1])
                elif op:
                    s = mult_cached(s,test_list[op_idx+1])
                else:
                    s = add_cached(s,test_list[op_idx+1])
            P(s)

            if s == test_product:
                P('works!')
                c += test_product
                break
            elif s > test_product:
                break
            P('                                             ')
        P('-----------------------------------------------')
        d += 1
    return c

@cache
def caten_cached(a,b):
    P(a,'||',b)
    return int(str(a) + '' + str(b))

@cache
def add_cached(a,b):
    P(a,'+',b)
    return a+b

@cache
def mult_cached(a,b):
    P(a,'*',b)
    return a*b


@cache
def add_set(tup):
    s = 0
    for i in tup:
        s += int(i)
    return s

@cache
def mult_set(tup):
    s = 1
    for i in tup:
        s = s * int(i)
    return s

def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)
    

def puzzle_text():
    print("""--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?


--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?

""")







#---------------------------------------------------------
def P(*args, force = False, end = False):
    if DEBUG or force:
        if len([*args]) > 1:
            if end:
                print(' '.join(str(x) for x in [*args]),end = end)
            else:
                pp.pprint([*args])
        else:
            if end:
                print(*args,end = end)
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
