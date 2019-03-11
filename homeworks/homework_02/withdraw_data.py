# returns list of lists that should be interpreted as rows of a table

import json
import csv
import copy


def test_data(table):
    s = ''
    length = -1
    for row in table:
        if (len(row) != length and length != -1):
            raise SystemExit
        length = len(row)
        l = copy.deepcopy(row)
        s += ''.join(l)
    if len(s) == 0:
        raise SystemExit


def receive_data(filename, enc, frmt):
    table = []
    if (frmt == 'json'):
        with open(filename, encoding=enc) as f:
            data = json.load(f)
            table_header = []
            table_content = []

            for column_name in data[0]:     # get table header from first dict
                table_header.append(column_name)

            for content in data:            # every row has same header
                if list(content.keys()) != table_header:
                    raise SystemExit

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
    test_data(table)

    return table
