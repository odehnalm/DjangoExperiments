# -*- coding: utf-8 -*-
import scrapy
# from scrapy_djangoitem import DjangoItem

# from apps.scrapy_model.models import Product


class ScrapyAppItem(scrapy.Item):
    nombre = scrapy.Field()
    ficha_tecnica = scrapy.Field()
    detalles = scrapy.Field()
    tiendas = scrapy.Field()
    store_id = scrapy.Field()
    job_id = scrapy.Field()
    category_id = scrapy.Field()


class BenchmarkScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    modelo = scrapy.Field()
    item_mark = scrapy.Field()
    serie = scrapy.Field()
