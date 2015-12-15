#!/usr/bin/env python

import unittest

import solver

GRID = [0b0010,
        0b1000,
        0b1101,
        0b0111]

class IsOddTest(unittest.TestCase):
    def test_default_case(self):
        self.failUnless(solver.set_n_bits(3)==7)
    def test_permute_row(self):
        permutes = solver.permute_row([1,3,2], 12)
        self.failUnless(True)
    def test_get_filtered_column_0(self):
        self.failUnless(solver.get_filtered_column(GRID,0,4)==0b0110)
    def test_get_filtered_column_1(self):
        self.failUnless(solver.get_filtered_column(GRID,1,4)==0b0011)
    def test_get_filtered_column_2(self):
        self.failUnless(solver.get_filtered_column(GRID,2,4)==0b1001)
    def test_get_filtered_column_3(self):
        self.failUnless(solver.get_filtered_column(GRID,3,4)==0b0011)
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
