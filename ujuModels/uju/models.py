# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 14:56
# @Author  : bocheng.wu
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=100)
    city_pinyin = models.CharField(max_length=20, unique=True)
    city_url = models.CharField(max_length=255)

    class Meta:
        app_label = 'uju'


class Region(models.Model):
    city_name = models.CharField(max_length=100)
    city_pinyin = models.CharField(max_length=20)
    city_url = models.CharField(max_length=255)
    region_name = models.CharField(max_length=100)
    region_pinyin = models.CharField(max_length=100)
    region_url = models.CharField(max_length=255)
    region_code = models.CharField(max_length=20)
    is_finish = models.BooleanField(default=False)

    class Meta:
        app_label = 'uju'
        unique_together = ("city_pinyin", "region_pinyin")
