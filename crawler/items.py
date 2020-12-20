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


# 纺织行情
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


# 实时汇率
class ExchangeRateItem(scrapy.Item):
    # 货币名
    currencyName = scrapy.Field()
    # 现汇买入价
    currencyBuy = scrapy.Field()
    # 现汇卖出价
    currencySell = scrapy.Field()
    # 现钞买入价
    cashBuy = scrapy.Field()
    # 现钞卖出价
    cashSell = scrapy.Field()
    # 中行折算价
    middle = scrapy.Field()
    # 发布日期
    publishDate = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()
    pass


# 远期汇率
class ForwardRateItem(scrapy.Item):
    # 货币名
    currencyName = scrapy.Field()
    # 货币代码
    currencyCode = scrapy.Field()
    # 交易期限
    exchangeHour = scrapy.Field()
    # 买入价
    buy = scrapy.Field()
    # 卖出价
    sell = scrapy.Field()
    # 中间价
    middle = scrapy.Field()
    # 汇率日期
    publishDate = scrapy.Field()
    pass
