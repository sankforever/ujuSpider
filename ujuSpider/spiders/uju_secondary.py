# -*- coding: utf-8 -*-
import json
import scrapy
import jsonpath
from ujuModels.uju.models import Region


class UjuSecondarySpider(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            'ujuSpider.pipelines.UjuMongoSpiderPipeline': 300,
        },
        "collection_name": "secondary_house",
        "CONCURRENT_REQUESTS": 6,
        "LOG_FILE": './logs/uju_secondary.log',
        'LOG_LEVEL': 'ERROR'
    }
    name = 'uju_secondary'
    allowed_domains = ['ujuz.cn']
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    def start_requests(self):
        querySet = Region.objects.filter(is_finish=False)
        for obj in querySet:
            page = 1
            self.crawler.stats.set_value(obj.id, "")
            url = f"https://m.ujuz.cn/ajax.php?city={obj.city_pinyin}&areas_pinyin={obj.region_pinyin}&areas={obj.region_code}&action=SecList&page={page}"
            yield scrapy.Request(url, meta={"obj": obj, "page": page}, dont_filter=True, headers=self.headers)

    def parse(self, response):
        obj = response.meta["obj"]
        page = response.meta["page"]
        response_data = json.loads(response.text)
        data = response_data["data"]
        if data:
            now_houseIdStr = ",".join(jsonpath.jsonpath(data, "$..Id"))
            last_houseIdStr = self.crawler.stats.get_value(obj.id)
            if now_houseIdStr != last_houseIdStr:
                self.crawler.stats.set_value(obj.id, now_houseIdStr)
                for _ in data:
                    _["_id"] = _.pop("Id")
                    yield _
                page += 1
                url = f"https://m.ujuz.cn/ajax.php?city={obj.city_pinyin}&areas_pinyin={obj.region_pinyin}&areas={obj.region_code}&action=SecList&page={page}"
                yield scrapy.Request(url, meta={"obj": obj, "page": page}, dont_filter=True, headers=self.headers,
                                     callback=self.parse)
            else:
                self.finish(obj)
        else:
            self.finish(obj)

    def finish(self, obj):
        obj.is_finish = True
        obj.save()
