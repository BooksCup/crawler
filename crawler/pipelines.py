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
        return item
