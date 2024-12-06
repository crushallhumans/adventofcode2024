# adventofcode 2024
# crushallhumans
# puzzle 6
# 12/6/2024

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
import copy
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2024'
DEBUG = False
TEST_INPUT_STRING_ONE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 41
TEST_TWO_RESULT = 6


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    grid_hash = {}
    guard_coord = [-1,-1]
    limit_y = len(param_set)
    limit_x = 0
    for y in range(limit_y):
        for x in range(len(param_set[y])):
            grid_coord = (x,y)
            grid_hash[grid_coord] = [param_set[y][x],0] #also a counter for path
            if grid_hash[grid_coord][0] == '^':
                guard_coord = [x,y]
            if not y:
                limit_x += 1
    directions = {
        0:  ( 0,-1),    #up, N
        90: ( 1, 0),    #right, E +90 
        180:( 0, 1),    #down, S +90
        270:(-1, 0)     #left, W +90
    }
    viable_loops = 0
    P('start: ',guard_coord)
    grid_hash = process_path(grid_hash,limit_x,limit_y,directions,guard_coord)[0]
    P(grid_hash)

    potential_blockers = []
    for k,v in grid_hash.items():
        if v[1]:
            c += 1
            potential_blockers.append(k)

    if is_two_star:
        c = 0
        d = 0
        f = len(potential_blockers)
        P(potential_blockers)
        for i in potential_blockers:
            P(d,'/',f,'added',i,force = True)
            test_grid = []
            test_grid = copy.deepcopy(grid_hash)
            test_grid[i][0] = '#'
            c += 1 if process_path(test_grid,limit_x,limit_y,directions,guard_coord,i)[1] else 0
            d += 1
    return c

def process_path(grid_hash,limit_x,limit_y,directions,guard_coord,inspect = False):
    direction = 0
    d = 0
    last_360_path = []
    curr_360_path = []
    start_guard_coord = guard_coord.copy()
    start_direction = 0
    last_360_path_to_from_start = []
    curr_360_path_to_from_start = []
    loop_rotations = 0
    loop_found = False
    while guard_in_room(guard_coord,limit_x,limit_y) and d < 1000000:
        curr_360_path.append(tuple(guard_coord))
        curr_360_path_to_from_start.append(tuple(guard_coord))
        grid_hash[tuple(guard_coord)][1] += 1
        next_coord = [
            guard_coord[0] + directions[direction][0],
            guard_coord[1] + directions[direction][1]
        ]
        next_move_ok = False
        e = 0
        while not next_move_ok and e < 5:
            #P('   ',next_coord)
            if not guard_in_room(next_coord,limit_x,limit_y):
                break
            if grid_hash[tuple(next_coord)][0] == '#':
                #P('rotate')
                direction += 90
                loop_rotations += 1
                if direction not in directions:
                    direction = 0
                if loop_rotations >= len(directions):
                    loop_rotations = 0
                    #P('last: ',last_360_path)
                    #P('curr: ',curr_360_path)
                    if (last_360_path == curr_360_path):
                        P('loop found!')
                        loop_found = True
                        d = 9999999999
                        break
                    last_360_path = curr_360_path.copy()
                    curr_360_path = []

                next_coord = [
                    guard_coord[0] + directions[direction][0],
                    guard_coord[1] + directions[direction][1]
                ]                    
            else:
                next_move_ok = True
            e += 1
        guard_coord = next_coord
        if guard_coord == start_guard_coord and direction == start_direction:
            if (last_360_path_to_from_start == curr_360_path_to_from_start):
                P('full loop found!')
                loop_found = True
                d = 9999999999
                break
            last_360_path_to_from_start = curr_360_path_to_from_start.copy()
            curr_360_path_to_from_start = []
        d += 1
    return [grid_hash,loop_found]


def guard_in_room(g,x,y):
    return (
        (x > g[0] > -1) and 
        (y > g[1] > -1)
    )


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)


def puzzle_text():
    print("""--- Day N: X ---

""")







#---------------------------------------------------------
def P(*args, force = False):
    if DEBUG or force:
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
