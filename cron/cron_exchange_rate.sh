#!/bin/sh
cd /home/scrapy/crawler
nohup scrapy crawl ExchangeRate  >../logs/exchange_rate.log 2>&1 &
