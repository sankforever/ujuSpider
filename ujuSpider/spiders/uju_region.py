# -*- coding: utf-8 -*-
import scrapy
import re
from ujuModels.uju.models import City


class UjuRegionSpider(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            'ujuSpider.pipelines.UjuSpiderPipeline': 300,
        }
    }
    name = 'uju_region'
    allowed_domains = ['ujuz.cn']
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    def start_requests(self):
        querySet = City.objects.all()
        for obj in querySet:
            url = obj.city_url + "seclist.html"
            yield scrapy.Request(url, meta={"obj": obj}, dont_filter=True, headers=self.headers)

    def parse(self, response):
        obj = response.meta["obj"]
        city_name = obj.city_name
        city_pinyin = obj.city_pinyin
        city_url = obj.city_url
        region_name_list = response.xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/ul/li/a/text()').extract()[1:]
        region_url_list = ["https://m.ujuz.cn" + _ for _ in response.xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/ul/li/a/@href').extract()[1:]]
        region_pinyin_list = [url.split('/')[-1].strip(".html") for url in region_url_list]
        region_compose = zip(region_name_list, region_pinyin_list, region_url_list)
        region_list = [dict(region_name=region_info[0], region_pinyin=region_info[1], region_url=region_info[2]) for
                       region_info in region_compose]
        for region_info in region_list:
            data = dict(
                city_name=city_name,
                city_pinyin=city_pinyin,
                city_url=city_url,
                region_name=region_info["region_name"],
                region_url=region_info["region_url"],
                region_pinyin=region_info["region_pinyin"],
            )
            url = region_info["region_url"]
            yield scrapy.Request(url, meta={"data": data}, dont_filter=True, headers=self.headers,
                                 callback=self.parse_region)

    def parse_region(self, response):
        data = response.meta["data"]
        region_code = re.search("areas=(\d+)", response.text).group(1)
        yield dict(data, region_code=region_code)
