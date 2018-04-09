# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml
from FR_libs.MAscraper.MAscraper.utils.html import html2list

class CarrefourSpider(scrapy.Spider):
    name = 'carrefour'
    allowed_domains = ['www.rueducommerce.fr']
    start_urls = ['']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(CarrefourSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        #nom_prod = response.xpath('//div[@class="summary"]/h2').extract()
        number_item = int(float(response.xpath('count(//div[@class="summary"]/h2)').extract()[0]))
        nom_prod = []
        for k in range(number_item):
            xpath_nom = 'normalize-space((//div[@class="summary"]/h2)['+str(k+1)+'])'
            nom_prod.append(response.xpath(xpath_nom).extract()[0])

        url_prod = response.xpath('//article/a/@href').extract()
        n = len(nom_prod)
        #n = int(float(response.xpath('count(//div[@class="designations"]/h2)').extract()[0]))

        for i in range(n):

            if i >= self.max_items:
                return
                #raise CloseSpider('bandwidth_exceeded')

            yield scrapy.Request('https://www.rueducommerce.fr' + url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        #Detalles
        detalles = html2list(response.xpath('//div[@class="flexGrid-box boxCol2 noPadding tab-desc"]')
                             .extract()[0].replace('\xa0',' ')).splitlines()
        detail_prod = [x for x in detalles if x != ''][2:]

        url_tienda = 'https://www.rueducommerce.fr' + response.meta['url_tienda']

        #Ficha Tecnica
        #print(int(float(response.xpath('count(//table[@id="blocAttributesContent"]/tbody/tr/td)').extract()[0])))
        num_fictec = int(float(response.xpath('count(//table[@id="blocAttributesContent"]/tbody/tr/td)').extract()[0])/2)
        ficha_tec={}
        for k in range(num_fictec):
            ficha_tec[response.xpath('normalize-space((//table[@id="blocAttributesContent"]/tbody/tr/td)['+str(2*k+1)+'])').extract()[0].replace('\xa0:','')] = \
                response.xpath('normalize-space((//table[@id="blocAttributesContent"]/tbody/tr/td)[' + str(2*k+2) + '])').extract()[0]

        #Tienda
        #print('precio:')
        #print(response.xpath('normalize-space((//div[@class="price main"])[2])').extract()[0].replace("\u20ac", ".") + ' EUR')
        precio = response.xpath('normalize-space((//div[@class="price main"])[2])').extract()[0].replace("\u20ac", ".") + ' EUR'
        tienda = [{
            'precio':precio,
            'nombre_tienda':'Carrefour',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item