# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml


class CdiscountSpider(scrapy.Spider):
    name = 'cdiscount'
    allowed_domains = ['www.cdiscount.com']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(CdiscountSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):
        item = MascraperItem()
        #nom_prod = response.xpath('//div[@class="cPdtItTit"]/text()').extract()
        nom_prod = response.xpath('//div[@class="prdtBTit"]/text()').extract()
        url_prod = response.xpath('//div[@class="prdtBloc"]/div/a/@href').extract()
        #url_prod = response.xpath('//li[@class="cPdtItem jsPdtItem"]/a/@href').extract()

        n = len(nom_prod)
        #n = int(float(response.xpath('count(//div[@class="designations"]/h2)').extract()[0]))

        for i in range(n):

            if i >= self.max_items:
                return
                #raise CloseSpider('bandwidth_exceeded')

            yield scrapy.Request(url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        #Detalles
        detail_count = int(float(response.xpath('count(//ul[@class="fpBulletPoint"]/li)').extract()[0]))
        detail_prod = []
        for k in range(detail_count):
            detail_xpath = '//ul[@class="fpBulletPoint"]/li[' +str(k+1)+ ']'
            detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])



        url_tienda = response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//tbody/tr/td[1]').extract())
        ficha_der = cleanhtml(response.xpath('//tbody/tr/td[2]').extract())
        ficha_tec={}
        for k in range(len(ficha_der)):
            if ficha_izq[k] == '' or ficha_der[k]=='\xa0':
                continue
            ficha_tec[ficha_izq[k]] = ficha_der[k]

        #Tienda
        precio = cleanhtml(response.xpath('//span[contains(@class,"fpPrice price jsMain")]').extract()[0]).replace("\u20ac", ".") + ' EUR'
        tienda = [{
            'precio':precio,
            'nombre_tienda':'Cdiscount',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item