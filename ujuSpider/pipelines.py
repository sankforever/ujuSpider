# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from django.conf import settings
from ujuModels.uju.models import City, Region
from pymongo.errors import DuplicateKeyError
from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem


class UjuSpiderPipeline(object):
    def __init__(self):
        self.model_map = {
            "uju_city": City,
            "uju_region": Region
        }

    def process_item(self, item, spider):
        model = self.model_map[spider.name]
        try:
            model.objects.create(**item)
            return item
        except IntegrityError:
            DropItem("already exists")


class UjuMongoSpiderPipeline(object):
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(settings.MONGO_URL)
        self.db = self.client['spider']
        self.collection = self.db[collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            collection_name=crawler.settings.get('collection_name')
        )

    def process_item(self, item, spider):
        try:
            self.collection.insert(item)
            return item
        except DuplicateKeyError:
            DropItem("already exists")

    def close_spider(self, spider):
        self.client.close()
