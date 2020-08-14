# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeavePriceItem(scrapy.Item):
    # 品名
    name = scrapy.Field()
    # 类别
    type = scrapy.Field()
    # 价格
    lastTrade = scrapy.Field()
    # 单位
    unit = scrapy.Field()
    # 涨跌
    change = scrapy.Field()
    # 报价日期
    date = scrapy.Field()

    pass
