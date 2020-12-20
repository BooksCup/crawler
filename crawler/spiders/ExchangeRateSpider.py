import scrapy

from scrapy.http import Request

from crawler.items import ExchangeRateItem


# 实时汇率
class ExchangeRateSpider(scrapy.Spider):
    name = "ExchangeRate"
    custom_settings = {
        'ITEM_PIPELINES': {'crawler.pipelines.ExchangeRatePipeline': 301},
    }
    start_urls = ['https://www.boc.cn/sourcedb/whpj/']

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def generate_url(self, i):
        if i == 1:
            return 'https://www.boc.cn/sourcedb/whpj/index.html'
        else:
            return 'https://www.boc.cn/sourcedb/whpj/index_' + str((i - 1)) + '.html'

    def start_requests(self):
        return [scrapy.Request("https://www.boc.cn/sourcedb/whpj/", headers=self.headers)]

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
            if datas is not None and len(datas) > 7:
                item = ExchangeRateItem()
                item['currencyName'] = datas[0].xpath('text()').extract_first()
                item['currencyBuy'] = datas[1].xpath('text()').extract_first()
                item['cashBuy'] = datas[2].xpath('text()').extract_first()
                item['currencySell'] = datas[3].xpath('text()').extract_first()
                item['cashSell'] = datas[4].xpath('text()').extract_first()
                item['middle'] = datas[5].xpath('text()').extract_first()
                item['publishDate'] = datas[6].xpath('text()').extract_first()
                item['publishTime'] = datas[7].xpath('text()').extract_first()
                yield item
