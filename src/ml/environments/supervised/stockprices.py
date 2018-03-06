import csv

with open('NAB.AX.csv', 'r') as f:
    reader = csv.reader(f)

    data = {}
    headers = ['open', 'high', 'low', 'close', 'adj-close', 'volume']
    for row in reader:
        val = {}
        for i in range(len(row)-1):
            val[headers[i]] = row[i+1]
        data[row[0]] = val
