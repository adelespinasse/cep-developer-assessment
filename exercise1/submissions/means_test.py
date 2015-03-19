#!python

import means
import testutil

import unittest

class TestCalculateMeansFromFile(unittest.TestCase):
  def test_calculateMeansFromFile(self):
    results = means.calculateMeansFromFile('../input/xl.csv')
    expected = testutil.loadCsvWithFloats('../output/mean.csv')
    testutil.assertListOfDictsAlmostEqual(self, expected, results)

if __name__ == "__main__":
  unittest.main()
