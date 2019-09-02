# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class CrawlAmazonSpider(scrapy.Spider):
    name = 'my_orders'
    allowed_domains = ['www.amazon.de']
    start_urls = ['http://www.amazon.de/']
    custom_settings = {
        'COOKIES_DEBUG': True,
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

    def parse(self, response):
        self.log('parse')
        login_url = response.xpath('//a[@id="nav-link-accountList"]/@href').extract_first()
        yield response.follow(login_url, callback=self.parse_login_email)

    def parse_login_email(self, response):
        self.log('parse_login_email')
        request = FormRequest.from_response(
            response,
            formdata = {'email': self.settings.get('AMAZON_LOGIN_EMAIL', '')},
            callback = self.parse_login_password
        )
        self.log(request.headers)
        yield request

    def parse_login_password(self, response):
        self.log('parse_login_password')
        request = FormRequest.from_response(
            response,
            formdata = {'password': self.settings.get('AMAZON_LOGIN_PASSWORD', '')},
            callback = self.parse_logged_in
        )
        yield request

    def parse_logged_in(self, response):
        self.log('parse_logged_in')
        orders_url = response.xpath('//a[@id="nav-orders"]/@href').extract_first()
        yield response.follow(orders_url, callback=self.parse_orders)

    def parse_orders(self, response):
        self.log('parse_orders')
        h1 = response.xpath('//h1').extract_first()
        self.log(h1)
