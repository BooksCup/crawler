import scrapy

from crawler.items import WeavePriceItem


# 纺织行情
class WeavePriceSpider(scrapy.Spider):
    name = "WeavePrice"
    custom_settings = {
        'ITEM_PIPELINES': {'crawler.pipelines.CrawlerPipeline': 300},
    }
    start_urls = ['https://www.tnc.com.cn/market/average-price.html']

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        return [scrapy.Request("https://www.tnc.com.cn/market/average-price.html", headers=self.headers)]

    def parse(self, response):
        markets = response.xpath('//div[@class="fl w670"]/div[@class="mb10"]')
        for market in markets:
            type = market.xpath('div[@class="tit-bg1"]/h3/text()').extract_first()
            prices = market.xpath('div[@class="price_list_in"]/table/tbody/tr')
            for price in prices:
                item = WeavePriceItem()
                goods = price.xpath('td//text()').extract()
                if goods is not None and len(goods) > 4:
                    name = goods[0]
                    lastTrade = goods[1]
                    unit = goods[2]
                    change = goods[3]
                    date = goods[4]
                    item['name'] = name
                    item['lastTrade'] = lastTrade
                    item['unit'] = unit
                    item['change'] = change
                    item['date'] = date
                    item['type'] = type
                    yield item
