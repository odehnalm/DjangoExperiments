# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre = scrapy.Field()
    ficha_tecnica = scrapy.Field()
    detalles = scrapy.Field()
    producto_extrangero = scrapy.Field()
    tiendas = scrapy.Field()

    pass
