# -*- coding: utf-8 -*-


BOT_NAME = 'amazon'

SPIDER_MODULES = ['amazon.spiders']
NEWSPIDER_MODULE = 'amazon.spiders'

# Disobey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable cookies
COOKIES_ENABLED = True

# Default Amazon login email address and password
# Override here or use command line setting parameters
AMAZON_LOGIN_EMAIL = None
AMAZON_LOGIN_PASSWORD = None
