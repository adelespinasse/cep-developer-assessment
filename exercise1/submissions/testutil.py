import csv

def assertListOfDictsAlmostEqual(testCase, expected, actual):
  """Asserts that two lists of dicts are approximately equal. Leaves
     room for floating point rounding errors. """
  testCase.assertEqual(len(expected), len(actual))
  for index in xrange(len(expected)):
    expectedRow = expected[index]
    actualRow = actual[index]
    testCase.assertEqual(set(expectedRow), set(actualRow))
    for key in expectedRow:
      testCase.assertAlmostEqual(expectedRow[key], actualRow[key], msg='row %d, column %s' % (index + 1, key) )

def toFloat(s):
  """Converts a string to float if possible; otherwise returns string unmodified."""
  try:
    return float(s)
  except ValueError:
    return s

def convertRowToFloats(row):
  """Converts to float all the strings in a dict that can be converted. Returns new dict."""
  return { key: toFloat(value) for key, value in row.iteritems() }

def convertAllToFloats(rows):
  """Runs all dicts in the given list through convertRowToFloats. Returns new list."""
  return [convertRowToFloats(row) for row in rows]

def loadCsvWithFloats(filename):
  """Loads a CSV file with labeled columns, converts all values to
     float than can be converted, and returns an array of dicts."""
  return convertAllToFloats(list(csv.DictReader(open(filename, 'rU'))))
