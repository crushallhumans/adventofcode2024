# adventofcode 2024
# crushallhumans
# puzzle 4
# 12/4/2024

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
import subprocess
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2024'
DEBUG = False
TEST_INPUT_STRING_ONE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 18
TEST_TWO_RESULT = 9

STEP_TIME = 0.00005

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [list(input_line.strip()) for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    x = 0
    y = len(param_set)-1
    word = 'AMS' if is_two_star else 'XMAS'
    subprocess.call('clear')
    for y in range(len(param_set)-1,-1,-1):
        for x in range(len(param_set[y])):
            j = param_set[y][x]
            if j == word[0]:
                if is_two_star:
                    c += star_search_two(param_set,x,y,word[1:],c)
                else:
                    c += star_search_one(param_set,x,y,word[1:],c)
            else:
                if DEBUG:
                    search_and_visualize(param_set,-3,-3,-3,-3,'XMAS',STEP_TIME,c,x,y)
            x += 1
        y -= 1
    return c


def star_search_one(grid,x_start,y_start,word_fragment,c):
    xdiff = [-1,0,1]
    ydiff = [-1,0,1]
    found = 0
    for y in ydiff:
        for x in xdiff:
            if x or y:
                search = True
                frag_match = list(word_fragment)
                x_search = x_start
                y_search = y_start
                while search and frag_match:
                    x_search += x
                    y_search += y
                    if DEBUG:
                        search_and_visualize(grid,x_search,y_search,x_start,y_start,frag_match,STEP_TIME,found+c)
                    if not coord_exists(grid,x_search,y_search):
                        search = False
                    else:
                        n = frag_match.pop(0)
                        if n != grid[y_search][x_search]:
                            search = False
                            if not frag_match: #fail on last letter
                                frag_match = 'FAIL'

                if not frag_match:
                    found += 1
                    time.sleep(STEP_TIME*1.5)
    return found


def star_search_two(grid,x_start,y_start,word_fragment,c):
    xdiff = [-1,1]
    ydiff = [-1,1]
    found = 0
    all_found = []
    for y in ydiff:
        for x in xdiff:
            if x or y:
                search = True
                frag_match = list(word_fragment)
                x_search = x_start
                y_search = y_start
                x_search += x
                y_search += y
                if DEBUG:
                    search_and_visualize(grid,x_search,y_search,x_start,y_start,frag_match,STEP_TIME*3,found+c)
                if coord_exists(grid,x_search,y_search):
                    all_found.append(grid[y_search][x_search])
    str_found = ''.join(all_found)
    valid = ['MSMS',
             'SSMM',
             'SMSM',
             'MMSS']
    if str_found in valid:
        found += 1
    return found


def search_and_visualize(grid,x2,y2,x1,y1,f,t,c,x3=-3,y3=-3):
    subprocess.call('clear')
    print(str(f))
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if coord_exists(grid,x,y):
                n = grid[y][x]
                if x == x2 and y == y2:
                    print('\033[41m',n,'\033[0m',sep='',end='')
                elif x == x1 and y == y1:
                    print('\033[42m',n,'\033[0m',sep='',end='')
                elif x == x3 and y == y3:
                    print('\033[43m',n,'\033[0m',sep='',end='')
                else:
                    print(n,end='')
        print('')
    print('')
    print(c)
    time.sleep(t)


def coord_exists(grid,x,y):
    return True if ((-1 < y < len(grid)) and (-1 < x < len(grid[y]))) else False


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)


def puzzle_text():
    print("""--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?


--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?""")







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
