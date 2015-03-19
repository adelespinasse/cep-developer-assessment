#!python

import sys
sys.path.append('../../exercise1/submissions') # ugh, sorry

import percentiles
import testutil

import unittest

class TestCalculatePercentilesFromFile(unittest.TestCase):
  def test_calculatePercentilesFromFile(self):
    results = percentiles.calculatePercentilesFromFile('../input/mean.csv')
    expected = testutil.loadCsvWithFloats('../output/pct.csv')
    testutil.assertListOfDictsAlmostEqual(self, expected, results)

if __name__ == "__main__":
  unittest.main()

