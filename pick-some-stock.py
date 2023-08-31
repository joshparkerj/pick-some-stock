from csv import DictReader
from collections.abc import Iterable
from numpy import random

with open('CRSP_Constituents.csv.old', newline='') as csv_file:
    reader: Iterable[dict] = DictReader(csv_file)
    old_total_market = [row for row in reader if row['Index Name'] == 'Total Market']

with open('CRSP_Constituents.csv.new', newline='') as csv_file:
    reader = DictReader(csv_file)
    new_total_market = [row for row in reader if row['Index Name'] == 'Total Market']

old_set = set(row['Ticker'] for row in old_total_market)
old_dict = {row['Ticker']: row for row in old_total_market}


def old(ticker):
    return old_dict[ticker]


def weight(row):
    return float(row['Weight'])


def old_weight(ticker):
    return weight(old(ticker))


def in_old(row):
    return row['Ticker'] in old_set


def ticker_weight(row):
    return row['Ticker'], weight(row) + (weight(row) - old_weight(row['Ticker']))


total_market = [ticker_weight(new_row) for new_row in new_total_market if in_old(new_row)]
total_market = [row for row in total_market if row[1] > 0]

a = [row[0] for row in total_market]
p = [row[1]**(1/3) for row in total_market]

sum_p = sum(p)

print(random.choice(a, size=2, replace=False, p=[x / sum_p for x in p]))
