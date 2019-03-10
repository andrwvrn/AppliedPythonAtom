# returns file format as a string

import json
import csv


def check_f(filename, enc):
    try:
        with open(filename, encoding=enc) as f:
            data = json.load(f)
            return 'json'

    except json.decoder.JSONDecodeError:
        pass

    with open(filename, encoding=enc) as f:
        data = csv.reader(f, delimiter='\t')
        length = -1
        for row in data:
            if (len(row) != length and length != -1):
                print('Формат не валиден')
                raise SystemExit
            length = len(row)
    return 'tsv'
