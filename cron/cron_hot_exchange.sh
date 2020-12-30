#!/bin/sh
cd /home/scrapy/crawler
nohup scrapy crawl HotExchange  >../logs/hot_exchange.log 2>&1 &
