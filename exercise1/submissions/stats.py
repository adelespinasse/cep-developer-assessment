#!python

""" Exercise 1, task 2 of the CEP developer assessment.
    Author: Alan deLespinasse (aldel@aldel.com) """

# NOTES: Based on the example output in ../output/stats.csv, I
# inferred that this task was meant to operate on the results of the
# first task (the means for each question), rather than finding stats
# for all of the raw data. For example, if the input was all of the
# raw data from task 1, the max for each question would be 7.
#
# The task description didn't mention calculating the standard
# deviation, but it was there in the sample output. Or rather, I
# assumed that the row labeled "std" was meant to be the standard
# deviation. The results I got for standard deviations didn't agree
# with the sample output, so maybe it was meant to be something else,
# or maybe I did the standard deviation calculation wrong. Anyway, I
# took the liberty of modifying the sample output file to provide a
# reference for the unit test.
#
# I also considered the possibility that it was meant to be the
# standard devation of all of the raw answers for each question,
# rather than of the means for the different clients, but that also
# didn't give the same results as the sample output file.
#
# Also, the description said to include the median. By some
# definitions, median would be the same as the 50th percentile, so
# would already be included. But the sample output file implies that
# percentiles should be calculated using the nearest rank method, by
# which the 50th pecentile is only the same as the median for odd
# sample sizes (assuming the median is, as usual, the mean of the two
# points nearest the center). So, if the sample size were even, the
# median would not be included.


import csv
import math

# Column names of survey questions on which to compute means. NOTE:
# The task description said the final column name should be "undrorg",
# but all example files use "impsust" instead. I took the liberty of
# using "impsust" to agree with the sample files, for easy
# verification of correct output.
questions = ['fldimp', 'undrfld', 'advknow', 'pubpol', 'comimp',
             'undrwr', 'undrsoc', 'orgimp', 'impsust']

def calculateStatsFromFile(filename):
  """Given the name of a CSV file, returns a list of stats.

     There's a result in the list for each statistic (count, mean,
     etc.). Each result is a dict, with values for each of the
     question labels listed in "questions" above.

     Each row also has a label under key '' (empty string).

     Example: the "count" row looks like this:

     { '': 'count', 'fldimp': 8, 'undrfld': 8, ...}

     indicating that there were 8 values for the 'fldimp' question, 8
     for the 'undrfld' question, etc.

     This allows easy dumping to a CSV file in the specified format.

     This function is not very fault tolerant. If any column values
     are missing or not properly formatted numbers, it's likely to
     throw an exception. If there are zero rows of input, it will
     divide by zero. """
  questionData = { q: [] for q in questions }
  with open(filename, 'rU') as csvfile:
    for row in csv.DictReader(csvfile):
      for question in questions:
        questionData[question].append(float(row[question]))

  for q in questions:
    questionData[q].sort()

  counts = { q: len(v) for q, v in questionData.iteritems() }
  means = { q: mean(v) for q, v in questionData.iteritems() }
  stddevs = { q: standardDev(v) for q, v in questionData.iteritems() }
  mins = { q: v[0] for q, v in questionData.iteritems() }
  q25s = { q: percentile(v, 25) for q, v in questionData.iteritems() }
  q50s = { q: percentile(v, 50) for q, v in questionData.iteritems() }
  q75s = { q: percentile(v, 75) for q, v in questionData.iteritems() }
  maxes = { q: v[-1] for q, v in questionData.iteritems() }

  # Ugly way to add a label to each row, for easy CSV output. The
  # first column in the output file is labeled with an empty string.
  counts[''] = 'count';
  means[''] = 'mean';
  stddevs[''] = 'std';
  mins[''] = 'min';
  q25s[''] = '25%';
  q50s[''] = '50%';
  q75s[''] = '75%';
  maxes[''] = 'max';
  return [counts, means, stddevs, mins, q25s, q50s, q75s, maxes]


def mean(data):
  """Returns the mean of a list of numbers. Will fail on an empty list
     (divide by zero)."""
  return sum(data) / float(len(data))

def standardDev(data):
  """Returns the standard deviation of a list of numbers. Will fail on
     an empty list (divide by zero)."""
  m = mean(data)
  return math.sqrt(sum([(x-m) * (x-m) for x in data]) / len(data))

def percentile(data, percent):
  """Calculates the given percentile of a sorted list, by the nearest
     rank method.

     data must be pre-sorted, and must not be empty. """
  rank = int(math.ceil(percent / 100.0 * len(data)))
  rank = max(rank, 1)
  rank = min(rank, len(data))
  return data[rank - 1]


if __name__ == "__main__":
  stats = calculateStatsFromFile('../output/mean.csv')
  with open('stats.csv', 'wt') as csvfile:
    # The first column in the output file is labeled with an empty
    # string.
    writer = csv.DictWriter(csvfile, [''] + questions, lineterminator='\n')
    writer.writeheader()
    writer.writerows(stats)
