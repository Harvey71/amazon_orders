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
            years[year] = 0.0
        years[year] += costs
for year in sorted(years.keys()):
    print('%s: %5.2f€' % (year, years[year]))
