import scrapy

from crawler.items import HotExchangeItem


# 热门汇率
class HotExchangeSpider(scrapy.Spider):
    name = "HotExchange"
    custom_settings = {
        'ITEM_PIPELINES': {'crawler.pipelines.HotExchangePipeline': 303},
    }
    start_urls = ['https://www.baidu.com/s?wd=%E7%BE%8E%E5%85%83%20%E4%BA%BA%E6%B0%91%E5%B8%81%E6%B1%87%E7%8E%87']

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        return [scrapy.Request(
            "https://www.baidu.com/s?wd=%E7%BE%8E%E5%85%83%20%E4%BA%BA%E6%B0%91%E5%B8%81%E6%B1%87%E7%8E%87",
            headers=self.headers)]

    def parse(self, response):
        item = HotExchangeItem()
        item['currencyName'] = "美元"
        current_price = response.xpath(
            '//span[@class="op-stockdynamic-cur-num c-gap-right-small"]/text()').extract_first()
        title_css = response.xpath('//div[@class="op-stockdynamic-cur"]/@style').extract_first()
        item['titleCss'] = title_css
        change = response.xpath('//span[@class="op-stockdynamic-cur-info c-gap-right-small"]/text()').extract_first()
        time = response.xpath('//div[@class="op-stockdynamic-update"]/text()').extract_first()
        item['currentPrice'] = current_price
        item['change'] = change
        item['createTime'] = str(time).strip()
        prices = response.xpath('//ul[@class="op-stockdynamic-info"]/li')
        for price in prices:
            title = price.xpath('span[@class="op-stockdynamic-info-name"]/text()').extract_first()
            value = price.xpath('span[@class="op-stockdynamic-info-value"]/text()').extract_first()
            css = price.xpath('span[@class="op-stockdynamic-info-value"]/@style').extract_first()
            if "今开" in title:
                print('今开:' + value)
                item['todayPrice'] = value
                item['todayPriceCss'] = css
            if "昨收" in title:
                print('昨收:' + value)
                print(css)
                item['yesterdayPrice'] = value
                item['yesterdayPriceCss'] = css
            if "最高" in title:
                print('最高:' + value)
                print(css)
                item['highestPrice'] = value
                item['highestPriceCss'] = css
            if "最低" in title:
                print('最低:' + value)
                print(css)
                item['lowestPrice'] = value
                item['lowestPriceCss'] = css
        yield item
