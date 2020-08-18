#!/bin/sh
cd /home/scrapy/crawler
nohup scrapy crawl WeavePrice  >../logs/weave_price.log 2>&1 &
