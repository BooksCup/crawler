#!/bin/sh
cd /home/scrapy/crawler
nohup scrapy crawl ForwardExchange  >../logs/forward_exchange.log 2>&1 &
