#!/bin/sh
cd /home/scrapy/crawler
nohup scrapy crawl WeavePrice  >../main.log 2>&1 &