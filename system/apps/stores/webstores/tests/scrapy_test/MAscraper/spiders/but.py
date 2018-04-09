# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml

class ButSpider(scrapy.Spider):
    name = 'but'
    allowed_domains = ['www.but.fr']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(ButSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        nom_prod = cleanhtml(response.xpath('//span[@class="product-title"]').extract())
        url_prod = response.xpath('//div[@class="product-whithout-odr"]/a/@href').extract()
        print(nom_prod)
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                return

            yield scrapy.Request('https://www.but.fr' + url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        #Detalles
        detail_count = int(float(response.xpath('count(//div[@class="product-note-list"]/ul/li)').extract()[0]))
        detail_prod = []
        for k in range(detail_count):
            detail_xpath = '////div[@class="product-note-list"]/ul/li[' +str(k+1)+ ']'
            detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])

        url_tienda = 'https://www.but.fr' + response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//ul[@class="details-heading-product"]/li/span[1]').extract())
        ficha_der = cleanhtml(response.xpath('//ul[@class="details-heading-product"]/li/span[2]').extract())
        ficha_tec={}
        for k in range(len(ficha_izq)):
            ficha_tec[ficha_izq[k]] = ficha_der[k]

        #Tienda
        precio = response.xpath('//p[@class="current-price"]/text()').extract()[0].replace("\u20ac", " EUR").replace(',','.')
        tienda = [{
            'precio':precio,
            'nombre_tienda':'But',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = re.sub('  +','',cleanhtml(nom_prod[counter]).replace('\n',''))
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item