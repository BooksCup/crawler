import scrapy

from scrapy.http import Request

from crawler.items import ForwardRateItem


# 远期汇率
class ForwardExchangeSpider(scrapy.Spider):
    name = "ForwardExchange"
    custom_settings = {
        'ITEM_PIPELINES': {'crawler.pipelines.ForwardRatePipeline': 302},
    }
    start_urls = ['https://www.boc.cn/sourcedb/ffx/']

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def generate_url(self, i):
        if i == 1:
            return 'https://www.boc.cn/sourcedb/ffx/index.html'
        else:
            return 'https://www.boc.cn/sourcedb/ffx/index_' + str((i - 1)) + '.html'

    def start_requests(self):
        return [scrapy.Request("https://www.boc.cn/sourcedb/ffx/", headers=self.headers)]

    def parse(self, response):
        totalPageNum = response.xpath('//div[@class="turn_page"]/p/span/text()').extract_first()
        for i in range(int(totalPageNum)):
            newUrl = self.generate_url(i + 1)
            print(newUrl)
            yield Request(newUrl,
                          headers=self.headers,
                          callback=self.parse_item)

    def parse_item(self, response):
        rates = response.xpath('//div[@class="publish"]/div[2]/table/tr')
        for rate in rates:
            datas = rate.xpath('td')
            if datas is not None and len(datas) > 6:
                item = ForwardRateItem()
                item['currencyName'] = datas[0].xpath('text()').extract_first()
                item['currencyCode'] = datas[1].xpath('text()').extract_first()
                item['exchangeHour'] = datas[2].xpath('text()').extract_first()
                item['buy'] = datas[3].xpath('text()').extract_first()
                item['sell'] = datas[4].xpath('text()').extract_first()
                item['middle'] = datas[5].xpath('text()').extract_first()
                item['publishDate'] = datas[6].xpath('text()').extract_first()
                yield item
