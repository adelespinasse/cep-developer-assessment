#!python

import stats
import testutil

import unittest

class TestCalculateStatsFromFile(unittest.TestCase):
  def test_calculateStatsFromFile(self):
    results = stats.calculateStatsFromFile('../output/mean.csv')
    expected = testutil.loadCsvWithFloats('../output/stats.csv')
    testutil.assertListOfDictsAlmostEqual(self, expected, results)

if __name__ == "__main__":
  unittest.main()
