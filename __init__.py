#!/usr/bin/env python

import sys
from solver import Grid
from data import *

def main():
    grid = Grid(HORIZONTAL_VALUES,VERTICAL_VALUES,FILTERED_GRID)
    before = grid.permute_rows()[:]
    after = grid.filter_rows()[:]
    for i in xrange(0,len(before)):
        permute_before = before[i]
        permute_after = after[i]
        
        print "len(permute_before) {0} len(permute_after) {1}".format(len(permute_before),len(permute_after))
    
    return 1

if __name__ == '__main__':
    sys.exit(not main())
