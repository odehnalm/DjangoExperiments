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


class CPUBenchmarkSpider(scrapy.Spider):
    name = 'CPU_Benchmark'
    allowed_domains = ['www.www.cpubenchmark.net']

    #Max items y Rotate Agent
    # max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(CPUBenchmarkSpider, self).__init__(*args, **kwargs)

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
        tipo_equipo = cleanhtml(response.xpath('//tr/td[11]').extract())

        # print(cleanhtml(response.xpath('//tr/td[11]').extract()))

        # print(cleanhtml(response.xpath('//tr/td[1]/a').extract()))

        for i in range(len(modelo)):

            #Si no es para laptops no lo agregamos
            if 'aptop' not in tipo_equipo[i]:
                continue

            #Series
            serie = ''

            #Intel
            if 'Intel' in modelo[i]:
                if 'ATOM' in modelo[i].upper(): serie = 'Atom'
                elif 'CELERON' in modelo[i].upper(): serie = 'Celeron'
                elif 'PENTIUM' in modelo[i].upper(): serie = 'Pentium'
                elif 'CORE2' in modelo[i].upper(): serie = 'Core2'
                elif 'CORE SOLO' in modelo[i].upper(): serie = 'Core Solo'
                elif 'CORE M3' in modelo[i].upper(): serie = 'Core M3'
                elif 'CORE M5' in modelo[i].upper(): serie = 'Core M5'
                elif 'CORE M7' in modelo[i].upper(): serie = 'Core M7'
                elif 'CORE M' in modelo[i].upper(): serie = 'Core M'
                elif 'CORE I3' in modelo[i].upper(): serie = 'Core i3'
                elif 'CORE I5' in modelo[i].upper(): serie = 'Core i5'
                elif 'CORE I7' in modelo[i].upper(): serie = 'Core i7'
                elif 'XEON' in modelo[i].upper(): serie = 'Xeon'

            #AMD
            if 'AMD' in modelo[i]:
                if 'OPTERON' in modelo[i].upper(): serie = 'Opteron'
                elif ' PRO' in modelo[i].upper(): serie = 'PRO'
                elif 'RYZEN' in modelo[i].upper(): serie = 'Ryzen'
                elif 'PHENOM' in modelo[i].upper(): serie = 'Phenom'
                elif 'SEMPRON' in modelo[i].upper(): serie = 'Sempron'
                elif 'TURION' in modelo[i].upper(): serie = 'Turion'
                elif 'ATHLON' in modelo[i].upper(): serie = 'Athlon'
                elif 'A4' in modelo[i].upper(): serie = 'A4'
                elif 'A6' in modelo[i].upper(): serie = 'A6'
                elif 'A8' in modelo[i].upper(): serie = 'A8'
                elif 'A9' in modelo[i].upper(): serie = 'A9'
                elif 'A10' in modelo[i].upper(): serie = 'A10'
                elif 'A12' in modelo[i].upper(): serie = 'A12'
                elif 'E1' in modelo[i].upper(): serie = 'E1'
                elif 'E2' in modelo[i].upper(): serie = 'E2'
                elif ' E-' in modelo[i].upper(): serie = 'E'
                elif 'FX' in modelo[i].upper(): serie = 'FX'
                elif ' G-' in modelo[i].upper(): serie = 'G'
                elif 'GX' in modelo[i].upper(): serie = 'GX'
                elif 'RX' in modelo[i].upper(): serie = 'RX'
                elif ' R-' in modelo[i].upper(): serie = 'R'


            item["modelo"] = modelo[i]
            item["item_mark"] = item_mark[i]
            item["serie"] = serie

            yield item
