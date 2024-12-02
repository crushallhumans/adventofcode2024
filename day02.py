# adventofcode 2024
# crushallhumans
# puzzle 2
# 12/2/2024

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
TEST_INPUT_STRING_ONE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 2
TEST_TWO_RESULT = 4


def reprocess_input(param_set):
    if isinstance(param_set,str):
        param_set = [re.split(r'\s+',input_line.strip()) for input_line in param_set.splitlines()]
        r = []
        for i in param_set:
            r.append( [int(x) for x in i] )
        return r
    else:
        return param_set


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)

    c = 0

    for i in param_set:
        unsafe_at_pos = evaluate_set_safeness(i)
        if is_two_star and unsafe_at_pos:
            for d in range(0,len(i)):
                ii = i.copy()
                ii.pop(d)
                unsafe_at_pos = evaluate_set_safeness(ii)
                P('retested at %d: '%d,ii,unsafe_at_pos)
                if not unsafe_at_pos:
                    break

        result = 1 if not unsafe_at_pos else 0
        c += result
        P("final result: ",'UNSAFE' if unsafe_at_pos else 'ok',c)
        P('')
        P('')
    return c


def evaluate_set_safeness(i):
    uppy = True if i[1] > i[0] else False
    down = not uppy
    if bad_equality(i[1],i[0]):
        P('unsafe at pos 1',i)
        return 1
    P(i,'down' if down else 'uppy')

    for d in range(1,len(i)):
        if is_unsafe(
            down,
            uppy,
            i[d],
            i[d-1]
        ):
            P('unsafe at pos %i' % d,i)
            return d
    return 0



def is_unsafe(down,uppy,a,b):
    P('down' if down else 'uppy',b,a,abs(a-b))
    if (
        (down and a > b)
        or
        (uppy and a < b)
        or
        bad_equality(a,b)
    ):
        P('unsafe')
        return True
    return False

def bad_equality(a,b):
    return (
        (a == b)
        or
        (not (4 > abs(a - b) > 0))
    )


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)


def puzzle_text():
    print("""--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
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
