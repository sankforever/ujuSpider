# -*- coding: utf-8 -*-
import scrapy


class UjuCitySpider(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            'ujuSpider.pipelines.UjuSpiderPipeline': 300,
        }
    }
    name = 'uju_city'
    allowed_domains = ['ujuz.cn']
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    def start_requests(self):
        url = "https://m.ujuz.cn/city.html"
        yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        city_name_list = response.xpath('//div[@class="box"]/ul/li/a/text()').extract()
        city_url_list = response.xpath('//div[@class="box"]/ul/li/a/@href').extract()
        city_pinyin_list = [url.split('/')[-2] for url in city_url_list]
        city_compose = zip(city_name_list, city_pinyin_list, city_url_list)
        city_list = [dict(city_name=city_info[0], city_pinyin=city_info[1], city_url=city_info[2]) for city_info in
                     city_compose]
        for city_info in city_list:
            yield city_info
