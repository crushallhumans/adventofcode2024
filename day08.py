# adventofcode 2024
# crushallhumans
# puzzle 8
# 12/8/2024

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
import numpy
from functools import reduce
from functools import cache
from itertools import chain
from itertools import product
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2024'
DEBUG = False
TEST_INPUT_STRING_ONE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 14
TEST_TWO_RESULT = 34


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
    limit_y = len(param_set)
    limit_x = 0
    antenna_sets = {}
    for y in range(limit_y):
        for x in range(len(param_set[y])):
            grid_coord = (x,y)
            grid_val = param_set[y][x]
            grid_hash[grid_coord] = [grid_val,{}] 
            if grid_val != '.':
                if grid_val not in antenna_sets:
                    antenna_sets[grid_val] = {'coords':[],'pairs':set()}
                antenna_sets[grid_val]['coords'].append(grid_coord)
            if not y:
                limit_x += 1
    for k,v in antenna_sets.items():
        x = list(product(v['coords'], repeat=2))
        for i in x:
            if i[0] != i[1]:
                a = i[0]
                b = i[1]
                if b < a:
                    a = i[1]
                    b = i[0]
                v['pairs'].add((
                    a,
                    b,
                ))
    P(antenna_sets)
    antinodes = set()
    for k,v in antenna_sets.items():
        P(k)
        for i in v['pairs']:
            P(i)
            a = i[0]
            b = i[1]
            subtr = tuple(x-y for x, y in zip(a, b))
            P('sub',subtr)

            steps = 1
            if is_two_star:
                steps = limit_x*limit_y
            off_up = False
            off_down = False
            antinode_up = [
                a[0],
                a[1]
            ]
            antinode_down = [
                b[0],
                b[1]
            ]
            if is_two_star:
                antinodes.add(tuple(antinode_up))
                antinodes.add(tuple(antinode_down))

            while steps > 0:
                P('step: ',steps)
                antinode_up = [
                    antinode_up[0] + subtr[0],
                    antinode_up[1] + subtr[1]
                ]
                antinode_down = [
                    antinode_down[0] + (-1 * subtr[0]),
                    antinode_down[1] + (-1 * subtr[1])
                ]
                if (
                    (limit_x > antinode_up[0] >= 0)
                    and
                    (limit_y > antinode_up[1] >= 0)
                ):
                    P(antinode_up)
                    antinodes.add(tuple(antinode_up))
                else:
                    off_up = True
                if (
                    (limit_x > antinode_down[0] >= 0)
                    and
                    (limit_y > antinode_down[1] >= 0)
                ):
                    P(antinode_down)
                    antinodes.add(tuple(antinode_down))
                else:
                    off_down = True
                steps -= 1
                if off_up and off_down:
                    break

    P(antinodes)
    return len(antinodes)


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)
    param_set = reprocess_input(param_set)
    c = 7777
    for i in param_set:
        continue
    return c


def puzzle_text():
    print("""--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?


--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?

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
