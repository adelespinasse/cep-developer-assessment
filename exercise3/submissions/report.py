#!python

""" Exercise 3 of the CEP developer assessment.
    Author: Alan deLespinasse (aldel@aldel.com) """

import csv
import json

# Column names of survey questions on which to compute means. NOTE:
# The task description said the final column name should be "undrorg",
# but all example files use "impsust" instead. I took the liberty of
# using "impsust" to agree with the sample files, for easy
# verification of correct output.
questions = ['fldimp', 'undrfld', 'advknow', 'pubpol', 'comimp',
             'undrwr', 'undrsoc', 'orgimp', 'impsust']


def getCsvRows(filename, keyColumn):
  """Loads a whole CSV file into a dict of dicts. Column labels should be in first row.

     filename: name of the file to load
     keyColumn: name of the column to use as key names """
  results = {}
  for row in csv.DictReader(open(filename, 'rU')):
    results[row[keyColumn]] = row
  return results


def createReportFromFiles(meanFilename, statsFilename, pctFilename, clientName):
  """Creates a JSON-serializable report for a given client.

     meanFilename: name of a file containing mean data for each client
     statsFilename: name of a file containing each of several stats for clients overall
     pctFilename: name of a file containing percentile data for each client
     clientName: name of the client """
  # This loads the entire files into dicts, then picks one row out of
  # each of the first two. This would be inefficient if the files were
  # very large; I'd instead write a function to load only one row in
  # the first place.
  means = getCsvRows(meanFilename, 'fdntext')[clientName]
  percentiles = getCsvRows(pctFilename, 'fdntext')[clientName]
  stats = getCsvRows(statsFilename, '')
  return {
    "version": "1.0",
    "reports": [
      {
        "name": clientName + " Report",
        "title": clientName + " Report",
        "cohorts": [],
        "segmentations": [],
        "elements": {
          question: {
            "type": "percentileChart",
            "absolutes": [
              stats['min'][question],
              stats['25%'][question],
              stats['50%'][question],
              stats['75%'][question],
              stats['max'][question]
              ],
            "current": {
              "name": "2014",
              "value": means[question],
              "percentage": percentiles[question]
              },
            "cohorts": [],
            "past_results": [],
            "segmentations": []
            }
            for question in questions
          }
        }
      ]
    }

if __name__ == "__main__":
  report = createReportFromFiles('../input/mean.csv', '../input/stats.csv',
                                 '../input/pct.csv', 'Tremont 14S')
  with open('output.json', 'w') as reportFile:
    json.dump(report, reportFile, indent=4)
