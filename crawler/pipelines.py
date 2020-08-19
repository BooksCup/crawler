# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time, datetime
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

        self.cur.execute("select 1 from t_weave_price_copy where price_type = %s and price_name = %s and price_date = %s",
                         (item['type'], item['name'],item['date']))
        result = self.cur.fetchone()
        if result:
            print('数据已存在')
        else:
            sql = 'insert into t_weave_price_copy(price_id, price_type, price_name, price_last_trade, price_unit, price_change, price_date, price_create_time)' \
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
