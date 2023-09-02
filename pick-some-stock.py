from csv import DictReader
from collections.abc import Iterable
from numpy.random import choice


def get_total_market_from_file(filename):
    with open(filename, newline='') as csv_file:
        reader: Iterable[dict] = DictReader(csv_file)
        return [stock for stock in reader if stock['Index Name'] == 'Total Market']


# the CRSP_Constituents.csv file comes from https://www.crsp.org/indexes-pages/returns-and-constituents
# (https://www.crsp.org/files/CRSP_Constituents.csv)
# I'm not sure whether historical files are available. For the old file, I use files I've downloaded previously
old_total_market = get_total_market_from_file('CRSP_Constituents.csv.old')
new_total_market = get_total_market_from_file('CRSP_Constituents.csv.new')
old_set = set(stock['Ticker'] for stock in old_total_market)
old_dict = {stock['Ticker']: stock for stock in old_total_market}

total_market = [
    (stock['Ticker'], 2 * float(stock['Weight']) - float(old_dict[stock['Ticker']]['Weight']))
    for stock in new_total_market if stock['Ticker'] in old_set
]

total_market = [stock for stock in total_market if stock[1] > 0]

a = [stock[0] for stock in total_market]
p = [stock[1] ** (1 / 3) for stock in total_market]

sum_p = sum(p)

print(choice(a, size=2, replace=False, p=[stock / sum_p for stock in p]))
