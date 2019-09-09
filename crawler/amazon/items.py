# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OrderItem(scrapy.Item):
    order_date = scrapy.Field()
    order_costs = scrapy.Field()
    order_number = scrapy.Field()
