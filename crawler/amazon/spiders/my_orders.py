# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import dateparser
import re
from ..items import OrderItem

class Rule():
    def __init__(self, allow = None, callback = None):
        self.allow = allow
        self.callback = callback

class OrdersSpider(scrapy.Spider):
    name = 'my_orders'
    allowed_domains = ['www.amazon.de']
    start_urls = ['http://www.amazon.de/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'DEFAULT_HEADERS': {
            'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'ACCEPT_ENCODING': 'gzip, deflate, br',
            'ACCEPT_LANGUAGE': 'de,en-US;q=0.7,en;q=0.3',
            'DNT': '1',
            'TE': 'trailers',
            'UPGRADE_INSECURE_REQUESTS': '1',
        }
    }
    rules = (
        Rule(allow=r'/ap/signin', callback='parse_login'),
        Rule(allow=r'/gp/.*/order-history', callback='parse_orders'),
        Rule(allow=r'.*', callback='parse_homepage')
    )
    logged_in = False

    def parse(self, response):
        for rule in self.rules:
            if re.search(rule.allow, response.url):
                yield from getattr(self, rule.callback)(response)
                break

    def parse_homepage(self, response):
        self.log('parse_homepage ' + str(self.logged_in))
        if not self.logged_in:
            # use login menu item
            url = response.xpath('//a[@id="nav-link-accountList"]/@href').extract_first()
        else:
            # use orders menu item
            url = response.xpath('//a[@id="nav-orders"]/@href').extract_first()
        yield response.follow(url)

    def parse_login(self, response):
        self.log('parse_login')
        request = FormRequest.from_response(
            response,
            formdata = {
                'email': self.settings.get('AMAZON_LOGIN_EMAIL', ''),
                'password': self.settings.get('AMAZON_LOGIN_PASSWORD', '')},
        )
        self.logged_in = True
        yield request

    def parse_orders(self, response):
        self.log('parse_orders')
        current_filter = response.xpath('//select[@id="orderFilter"]/option/@selected/parent::*/@value').extract_first()
        if not re.match(r'year-\d\d\d\d', current_filter):
            years = response.xpath('//select[@id="orderFilter"]/option/@value').re(r'year-\d\d\d\d')
            for year in years:
                request = FormRequest.from_response(
                    response,
                    formid='timePeriodForm',
                    formdata= {'orderFilter': year}
                )
                yield request
        else:
            orders = response.xpath('//div[@class="a-box-group a-spacing-base order"]')
            for order in orders:
                self.log('order')
                order_info  = order.xpath('.//div[contains(@class," order-info")]')
                shipment_info = order.xpath('./div/div[@class="a-box shipment"]')
                order_vals = order_info.xpath('.//span[@class="a-color-secondary value"]/text()').extract()
                order_date = dateparser.parse(order_vals[0].strip())
                order_costs = float(order_vals[1].strip().replace('EUR', '').replace(',', '.'))
                order_number = order_vals[2].strip()
                yield OrderItem(
                    order_date=order_date,
                    order_costs=order_costs,
                    order_number=order_number
                )
            next_url = response.xpath('//li[@class="a-last"]//a/@href').extract_first()
            if next_url:
                yield response.follow(next_url)


