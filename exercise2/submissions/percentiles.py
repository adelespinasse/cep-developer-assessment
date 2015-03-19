#!python

""" Exercise 2 of the CEP developer assessment.
    Author: Alan deLespinasse (aldel@aldel.com) """

import csv

# Column names of survey questions on which to compute means. NOTE:
# The task description said the final column name should be "undrorg",
# but all example files use "impsust" instead. I took the liberty of
# using "impsust" to agree with the sample files, for easy
# verification of correct output.
questions = ['fldimp', 'undrfld', 'advknow', 'pubpol', 'comimp',
             'undrwr', 'undrsoc', 'orgimp', 'impsust']

def calculatePercentilesFromFile(filename):
  """Given the name of a CSV file, returns the percentile of each client's mean
     rating for each survey question.

     File is assumed to contain a column named "fdntext" which
     contains the name of a client, and columns for each of the
     questions listed above in the "questions" list. Other columns are
     ignored.

     This function is not fault-tolerant for files that don't contain the
     expected columns, don't have a properly formatted number for
     every data point, or have zero rows of data.

     Output is ready for writing back to a CSV file. """
  clients = {}
  questionData = { q: [] for q in questions }
  with open(filename, 'rU') as csvfile:
    for row in csv.DictReader(csvfile):
      clients[row['fdntext']] = row
      for question in questions:
        questionData[question].append(float(row[question]))

  for q in questions:
    questionData[q].sort()

  # Return the results sorted by client name, so the order is predictable.
  clientNames = clients.keys()
  clientNames.sort()

  results = []
  for clientName in clientNames:
    client = clients[clientName]
    for question in questions:
      client[question] = percentileWithin(float(client[question]), questionData[question])
    results.append(client)

  return results


def percentileWithin(x, data):
  """Returns the percentile of a value within a sorted list of
     values. The value MUST appear in the list. """
  # NOTE: I would have thought that, for example, the lowest data
  # point would be percentile zero, but the sample output makes it
  # clear that it's expected to be 100 * 0.5 / N, so that's what I'm
  # doing.
  return 100.0 * (data.index(x) + 0.5) / len(data)


if __name__ == "__main__":
  percentiles = calculatePercentilesFromFile('../input/mean.csv')
  with open('pct.csv', 'wt') as csvfile:
    writer = csv.DictWriter(csvfile, ['fdntext'] + questions, lineterminator='\n')
    writer.writeheader()
    writer.writerows(percentiles)
