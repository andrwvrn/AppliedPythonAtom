# returns list of strings


def draw_table(table):

    # find max column lengths
    column_lengths = dict.fromkeys([i for i in range(len(table[0]))], -1)
    for row in table:
        for i in range(len(row)):
            if (column_lengths.get(i) and len(row[i]) > column_lengths[i]):
                column_lengths[i] = len(row[i])

    # form columns
    for row in table:
        if (table.index(row) != 0):
            for i in range(len(row)):
                if (i == len(row) - 1):   # last column
                    row[i] = '|  ' + ' '*(column_lengths[i] - len(row[i]))\
                             + row[i] + '  |'
                else:                     # other columns
                    row[i] = '|  ' + row[i] + ' '*(column_lengths[i] -
                                                   len(row[i])) + '  '

        else:
            for i in range(len(row)):

                s = (column_lengths[i] - len(row[i]))//2

                if (i == len(row) - 1):       # last column first row
                    if ((column_lengths[i] - len(row[i])) % 2 == 0):
                        row[i] = '|  ' + ' '*s + row[i] + ' '*s + '  |'
                    else:
                        row[i] = '|  ' + ' '*s + row[i] + ' '*(s+1) + '  |'
                else:                         # other columns first row
                    if ((column_lengths[i] - len(row[i])) % 2 == 0):
                        row[i] = '|  ' + ' '*s + row[i] + ' '*s + '  '
                    else:
                        row[i] = '|  ' + ' '*s + row[i] + ' '*(s+1) + '  '

    added_symbols = (len(table[0]) - 1) * 5 + 6
    table_length = sum(column_lengths.values()) + added_symbols

    table.append('-'*table_length)
    table.insert(0, '-'*table_length)
    return table
