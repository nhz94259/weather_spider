# -*- coding: utf-8 -*-
import scrapy
from  weather_spider.items import WeatherItem

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.weather.com.cn/weather/101220101.shtml']
    start_urls = ['http://www.weather.com.cn/weather/101220101.shtml']

    def parse(self, response):
        items = []
        day = response.xpath('//ul[@class="t clearfix"]')
        for i in list(range(7)):
            # 先申请一个weatheritem 的类型来保存结果
            item = WeatherItem()
            # 观察网页，并找到需要的数据
            item['date'] = day.xpath('./li[' + str(i + 1) + ']/h1//text()').extract()[0]
            item['temperature'] = day.xpath('./li[' + str(i + 1) + ']/p[@class="tem"]/i/text()').extract()[0]
            item['weather'] = day.xpath('./li[' + str(i + 1) + ']/p[@class="wea"]/text()').extract()[0]
            item['wind'] = day.xpath('./li[' + str(i + 1) + ']/p[@class="win"]/em/span/@title').extract()[0] + \
                           day.xpath('./li[' + str(i + 1) + ']/p[@class="win"]/i/text()').extract()[0]
            print(item)
            items.append(item)

        return items
