import sys
import check_encoding as ce
import check_format as cf
import withdraw_data as wd
import construct_table as ct


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Файл не валиден')
        raise SystemExit

    try:
        with open(filename, 'rb') as f:
            pass
    except FileNotFoundError:
        print('Файл не валиден')
        raise SystemExit

    try:

        enc = ce.check_e(filename)
        frmt = cf.check_f(filename, enc)
        data = wd.receive_data(filename, enc, frmt)
        table = ct.draw_table(data)

        for row in table:
            print(''.join(row))

    except SystemExit:
        print("Формат не валиден")
