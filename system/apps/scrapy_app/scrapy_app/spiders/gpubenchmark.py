# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from ..items import BenchmarkScraperItem


def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')

    if isinstance(raw_html, str):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    if isinstance(raw_html, list):
        cleantext = [re.sub(cleanr, '', componente) for componente in raw_html]
        return cleantext


class GPUBenchmarkSpider(scrapy.Spider):
    name = 'GPU_Benchmark'
    allowed_domains = ['www.www.gpubenchmark.net']

    #Max items y Rotate Agent
    # max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(GPUBenchmarkSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = BenchmarkScraperItem()
        modelo = cleanhtml(response.xpath('//tr/td[1]/a').extract())
        modelo = [x for x in modelo if x]
        item_mark = cleanhtml(response.xpath('//tr/td[3]').extract())
        tipo_equipo = cleanhtml(response.xpath('//tr/td[9]').extract())

        for i in range(len(modelo)):

            #Si no es para laptops no lo agregamos
            if 'obile' not in tipo_equipo[i] and 'nknown' not in tipo_equipo[i]:
                continue

            #Series
            serie = ''

            if 'GEFORCE' in modelo[i].upper(): serie = 'GeForce'
            elif 'RADEON' in modelo[i].upper(): serie = 'Radeon'
            elif 'FIREPRO' in modelo[i].upper(): serie = 'Firepro'
            elif 'IRIS' in modelo[i].upper(): serie = 'Iris'
            elif 'QUADRO' in modelo[i].upper(): serie = 'Quadro'

            item["modelo"] = modelo[i]
            item["item_mark"] = item_mark[i]
            item["serie"] = serie

            yield item