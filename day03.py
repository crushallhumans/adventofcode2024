# adventofcode 2024
# crushallhumans
# puzzle 3
# 12/3/2024

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
TEST_INPUT_STRING_ONE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_INPUT_STRING_TWO = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
TEST_ONE_RESULT = 161
TEST_TWO_RESULT = 48


def reprocess_input(param_set):
    if isinstance(param_set,str):
        ll = [input_line.strip() for input_line in param_set.splitlines()]
        l = ''
        for i in ll:
            l += i
        return(l)
    return param_set    


def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    r = re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)',param_set)
    for i in r:
        ii = re.findall(r'\d+',i)
        c += int(ii[0]) * int(ii[1])      
    return c

def two_star(param_set):
    print("---------------two_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    mults = {}
    onn_idx = []
    off_idx = []
    for match in re.finditer(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)',param_set):
        mults[match.start()] = int(match.group(1)) * int(match.group(2))
    for match in re.finditer(r'do\(\)',param_set):
        onn_idx.append(match.start())    
    for match in re.finditer(r"don't\(\)",param_set):
        off_idx.append(match.start())    
    onn = True
    for i in range(len(param_set)):
        if i in onn_idx:
            onn = True
        elif i in off_idx:
            onn = False
        if onn and i in mults.keys():
            c += mults[i]
    return c


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
        DEBUG = True

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
