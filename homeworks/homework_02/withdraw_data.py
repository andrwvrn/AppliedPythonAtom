# returns list of lists that should be interpreted as rows of a table

import json
import csv


def receive_data(filename, enc, frmt):
    table = []
    if (frmt == 'json'):
        with open(filename, encoding=enc) as f:
            data = json.load(f)
            table_header = []
            table_content = []
            for column_name in data[0]:
                table_header.append(column_name)
            table.append(table_header)
            for content in data:
                table_content = [value for value in content.values()]
                table.append(table_content)
            for i in range(len(table)):
                for j in range(len(table[i])):
                    table[i][j] = str(table[i][j])

    elif (frmt == 'tsv'):
        with open(filename, encoding=enc) as f:
            data = csv.reader(f, delimiter='\t')
            for row in data:
                table.append(row)

    return table
