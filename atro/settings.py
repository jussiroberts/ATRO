# -*- coding: utf-8 -*-

# Scrapy settings for atro project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'atro'

SPIDER_MODULES = ['atro.spiders']
NEWSPIDER_MODULE = 'atro.spiders'
COOKIES_ENABLED = False
#DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = True
USER_AGENT = 'atro (+http://www.artemisproject.org/)'
ITEM_PIPELINES = {
    'atro.pipelines.AtroPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent

