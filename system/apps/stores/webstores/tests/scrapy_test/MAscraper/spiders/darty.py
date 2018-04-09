# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml

class DartySpider(scrapy.Spider):
    name = 'darty'
    allowed_domains = ['www.darty.com']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(DartySpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        nom_prod = cleanhtml(response.xpath('//div[@class="prd-name"]').extract())
        print()
        print(nom_prod)
        print()
        detail_prod = cleanhtml(response.xpath('//ul[@class="infos_strenghts"]').extract())
        print(detail_prod)
        print()
        url_prod = response.xpath('//div[@class="prd-name"]/a/@href').extract()
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                return
                #raise CloseSpider('bandwidth_exceeded')

            yield scrapy.Request('https://www.darty.com' + url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'detail_prod': detail_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        detail_prod = response.meta['detail_prod']
        counter = response.meta['counter']
        url_tienda = 'https://www.darty.com' + response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//table[contains(@class,"font-2")]/tbody/tr/th[descendant-or-self::text()]').extract())
        ficha_der = cleanhtml(response.xpath('//*[@id="product_caracteristics"]/div[2]/table/tbody/tr/td').extract())
        ficha_tec={}
        for k in range(len(ficha_der)):
            if ficha_der[k] == '&amp;nbsp':
                continue
            ficha_tec[ficha_izq[k]] = ficha_der[k]

        #Tienda
        tienda = [{
            'precio': response.xpath('normalize-space(//div[@class="product_price font-2-b"])').extract()[0].replace(
                "\u20ac", " EUR").replace(",", ".").replace('\xa0',''),
            'nombre_tienda':'Darty', 'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['tiendas'] = tienda
        item['nombre'] = nom_prod[counter]
        item['detalles'] = cleanhtml(detail_prod[counter]).splitlines()[1:]
        item['ficha_tecnica'] = ficha_tec

        yield item