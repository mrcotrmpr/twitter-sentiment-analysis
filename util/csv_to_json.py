import csv
import json

csvfile = open('data/file.csv', 'r')
jsonfile = open('data/file.json', 'w')

fieldnames = ("text", "sentiment")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    if row["sentiment"].isnumeric():
        json.dump(row, jsonfile)
        jsonfile.write(',\n')
