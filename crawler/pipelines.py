# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import uuid

import pymysql

from crawler import settings


class CrawlerPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute(
            "select 1 from t_weave_price where price_type = %s and price_name = %s and price_date = %s",
            (item['type'], item['name'], item['date']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            sql = 'insert into t_weave_price(price_id, price_type, price_name, price_last_trade, price_unit, price_change, price_date, price_create_time)' \
                  ' values(%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (
                str(uuid.uuid1()).replace("-", ""),
                item['type'],
                item['name'],
                item['lastTrade'],
                item['unit'],
                item['change'],
                item['date'],
                create_time
            )
            self.cur.execute(sql, data)
            self.client.commit()

        self.cur.execute("select 1 from t_trade_moments where moments_type = %s and moments_date = %s",
                         ('0', item['date']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            date_pretty = str(datetime.datetime.now().month) + '月' + str(datetime.datetime.now().day) + '日'
            moments_data = (
                str(uuid.uuid1()).replace("-", ""),
                '0',
                '',
                date_pretty + ' 原材料行情',
                '包括化纤 纱线的今日价格',
                item['date'],
                create_time
            )
            self.cur.execute(
                "insert into t_trade_moments(moments_id, moments_type, moments_image, moments_title, moments_content, moments_date, moments_create_time) values(%s, %s, %s, %s, %s, %s, %s)",
                moments_data)
            self.client.commit()
        return item


class ExchangeRatePipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute("select 1 from t_exchange_rate where rate_currency_name = %s and rate_publish_time = %s",
                         (item['currencyName'], item['publishTime']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            sql = 'insert into t_exchange_rate(rate_id, rate_currency_name, rate_currency_buy, rate_currency_sell, rate_cash_buy, rate_cash_sell, rate_middle, rate_publish_date, rate_publish_time, rate_create_time)' \
                  ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (
                str(uuid.uuid1()).replace("-", ""),
                item['currencyName'],
                item['currencyBuy'],
                item['currencySell'],
                item['cashBuy'],
                item['cashSell'],
                item['middle'],
                item['publishDate'],
                item['publishTime'],
                create_time
            )
            self.cur.execute(sql, data)
            self.client.commit()

        self.cur.execute("select 1 from t_trade_moments where moments_type = %s and moments_date = %s",
                         ('1', create_date))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            date_pretty = str(datetime.datetime.now().month) + '月' + str(datetime.datetime.now().day) + '日'
            moments_data = (
                str(uuid.uuid1()).replace("-", ""),
                '1',
                '',
                date_pretty + ' 实时汇率',
                '包括美元,英镑,新台币,欧元等实时汇率',
                create_date,
                create_time
            )
            self.cur.execute(
                "insert into t_trade_moments(moments_id, moments_type, moments_image, moments_title, moments_content, moments_date, moments_create_time) values(%s, %s, %s, %s, %s, %s, %s)",
                moments_data)
            self.client.commit()
        return item


class ForwardRatePipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        create_date = datetime.datetime.now().strftime("%Y-%m-%d")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute(
            "select 1 from t_forward_exchange where currency_name = %s and exchange_hour = %s and publish_date = %s",
            (item['currencyName'], item['exchangeHour'], item['publishDate']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            sql = 'insert into t_forward_exchange(' \
                  'id,' \
                  ' currency_name,' \
                  ' currency_code,' \
                  ' exchange_hour,' \
                  ' buy,' \
                  ' sell,' \
                  ' middle,' \
                  ' publish_date,' \
                  ' create_time' \
                  ')' \
                  ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (
                str(uuid.uuid1()).replace("-", ""),
                item['currencyName'],
                item['currencyCode'],
                item['exchangeHour'],
                item['buy'],
                item['sell'],
                item['middle'],
                item['publishDate'],
                create_time
            )
            self.cur.execute(sql, data)
            self.client.commit()
        return item


class HotExchangePipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        self.cur.execute(
            "select 1 from t_hot_exchange where currency_name = %s and create_time = %s",
            (item['currencyName'], item['createTime']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            sql = 'insert into t_hot_exchange(' \
                  'id,' \
                  ' currency_name,' \
                  ' current_price,' \
                  ' price_change,' \
                  ' today_price,' \
                  ' yesterday_price,' \
                  ' highest_price,' \
                  ' lowest_price,' \
                  ' create_time,' \
                  ' title_css,' \
                  ' today_price_css,' \
                  ' yesterday_price_css,' \
                  ' highest_price_css,' \
                  ' lowest_price_css' \
                  ')' \
                  ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (
                str(uuid.uuid1()).replace("-", ""),
                item['currencyName'],
                item['currentPrice'],
                item['change'],
                item['todayPrice'],
                item['yesterdayPrice'],
                item['highestPrice'],
                item['lowestPrice'],
                item['createTime'],
                item['titleCss'],
                item['todayPriceCss'],
                item['yesterdayPriceCss'],
                item['highestPriceCss'],
                item['lowestPriceCss']
            )
            self.cur.execute(sql, data)
            self.client.commit()
        return item
