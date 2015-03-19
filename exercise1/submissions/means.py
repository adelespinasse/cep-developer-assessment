#!python

""" Exercise 1, task 1 of the CEP developer assessment.
    Author: Alan deLespinasse (aldel@aldel.com) """

import csv

# Column names of survey questions on which to compute means. NOTE:
# The task description said the final column name should be "undrorg",
# but all example files use "impsust" instead. I took the liberty of
# using "impsust" to agree with the sample files, for easy
# verification of correct output.
questions = ['fldimp', 'undrfld', 'advknow', 'pubpol', 'comimp',
             'undrwr', 'undrsoc', 'orgimp', 'impsust']

def calculateMeansFromFile(filename):
  """Given the name of a CSV file, returns mean ratings on certain
     survey questions for each client.

     File is assumed to contain a column named "fdntext" which
     contains the name of a client, and columns for each of the
     questions listed above in the "questions" list. Other columns are
     ignored. (This function is not fault-tolerant for files that
     don't contain the expected columns.)

     Returns an array of dicts, one dict per client, ready for writing
     back to a CSV file. Each dict contains the client name in field
     "fdntext" and the mean for each question. """
  clients = {}

  with open(filename, 'rU') as csvfile:
    for row in csv.DictReader(csvfile):
      clientName = row['fdntext']
      if not clientName in clients:
        # Initialize stats for client, if we haven't seen this client name before.
        clients[clientName] = { q: {'total': 0, 'count': 0} for q in questions }
      for question in questions:
        # Ignore any values that aren't normal ratings from 1 to 7.
        try:
          rating = int(row[question])
        except ValueError:
          continue
        if rating < 1 or rating > 7:
          continue
        stats = clients[clientName][question]
        stats['total'] = stats['total'] + rating
        stats['count'] = stats['count'] + 1

  # Return the results sorted by client name, so the order is predictable.
  clientNames = clients.keys()
  clientNames.sort()

  results = []
  for clientName in clientNames:
    row = { q: mean(clients[clientName][q]) for q in questions }
    row['fdntext'] = clientName
    results.append(row)
  return results

def mean(question):
  """Calculate the mean, given a dict containing a total of all
     ratings (question['total']) and the number of ratings
     (question['count']). Returns zero if count is zero. """
  try:
    return float(question['total']) / question['count']
  except ZeroDivisionError:
    return 0


if __name__ == "__main__":
  meansData = calculateMeansFromFile('../input/xl.csv')
  with open('mean.csv', 'wt') as csvfile:
    writer = csv.DictWriter(csvfile, ['fdntext'] + questions, lineterminator='\n')
    writer.writeheader()
    writer.writerows(meansData)
