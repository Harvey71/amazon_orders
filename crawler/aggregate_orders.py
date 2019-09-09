# -*- coding: utf-8 -*-
import json

years = dict()
with open('orders.jl', 'r') as f:
    lines = f.readlines()
    for line in lines:
        obj = json.loads(line)
        year =  obj['order_date'][:4]
        costs = obj['order_costs']
        if not year in years:
            years[year] = {'costs': 0.0, 'count': 0}
        years[year]['costs'] += costs
        years[year]['count'] += 1
total_count = 0
total_costs = 0.0
for year in sorted(years.keys()):
    costs = years[year]['costs']
    count = years[year]['count']
    print('%s:  %4d Bestellungen, %8.2f€ Kosten' % (year, count, costs))
    total_count += count
    total_costs += costs
print('-' * 42)
print('gesamt %4d Bestellungen, %8.2f€ Kosten' % (total_count, total_costs))
