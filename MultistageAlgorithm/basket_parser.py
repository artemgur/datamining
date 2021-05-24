from python_linq import From


# Parses transactions.csv file
def parse_csv(filename: str) -> From:
    return From(open(filename, 'r'))\
        .skip(1)\
        .select(lambda x: x.split(';'))\
        .groupBy(lambda key: key[1], lambda value: int(value[0][3:]))\
        .select(lambda x: list(x))
