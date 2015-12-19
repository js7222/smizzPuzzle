#!/usr/bin/env python

import sys
from solver import Grid
from data import *

def main():
    grid = Grid(HORIZONTAL_VALUES,VERTICAL_VALUES,FILTERED_GRID)
    grid.calculate()
    grid2 = Grid(HORIZONTAL_VALUES,VERTICAL_VALUES,grid.filtered_grid)
    
    return 1

if __name__ == '__main__':
    sys.exit(not main())
