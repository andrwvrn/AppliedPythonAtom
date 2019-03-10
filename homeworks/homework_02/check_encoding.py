# returns file encoding as a string


def check_e(filename):
    for enc in ('utf-8', 'utf-16', 'cp1251'):
        try:
            with open(filename, encoding=enc) as f:
                data = f.read(10)
                return enc
        except (UnicodeDecodeError, UnicodeError):
            pass
    raise SystemExit('Файл не валиден')
