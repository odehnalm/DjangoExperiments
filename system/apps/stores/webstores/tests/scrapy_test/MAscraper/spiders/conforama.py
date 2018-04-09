# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml

class ConforamaSpider(scrapy.Spider):
    name = 'conforama'
    allowed_domains = ['www.conforama.fr']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(ConforamaSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        #nom_prod = response.xpath('normalize-space(//h3[@class="itemTitle titleGB"])').extract()
        number_item = int(float(response.xpath('count(//h3[@class="itemTitle titleGB"])').extract()[0]))
        nom_prod = []
        for k in range(number_item):
            xpath_nom = 'normalize-space((//h3[@class="itemTitle titleGB"])['+str(k+1)+'])'
            nom_prod.append(response.xpath(xpath_nom).extract()[0])

        url_prod = response.xpath('//h3[@class="itemTitle titleGB"]/a[1]/@href').extract()
        #print(nom_prod)
        n = len(nom_prod)
        #n = int(float(response.xpath('count(//div[@class="designations"]/h2)').extract()[0]))

        for i in range(n):

            if i >= self.max_items:
                return
                #raise CloseSpider('bandwidth_exceeded')

            yield scrapy.Request('https://www.conforama.fr' + url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        #Detalles
        #print(response.xpath('count(//ul[@class="pointForts"]/li)').extract()[0])
        detail_count = int(float(response.xpath('count(//ul[@class="pointForts"]/li)').extract()[0]))
        detail_prod = []
        for k in range(detail_count):
            detail_xpath = '//ul[@class="pointForts"]/li[' +str(k+1)+ ']'
            detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])



        url_tienda = 'https://www.conforama.fr' + response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//td[contains(@class,"productSpecificationsLab")]').extract())
        ficha_der = cleanhtml(response.xpath('//td[contains(@class,"productSpecificationsVal")]/text()').extract())
        ficha_tec={}
        for k in range(len(ficha_izq)):
            ficha_tec[ficha_izq[k]] = re.sub(r"[\n\t]*", "",ficha_der[k])

        #Tienda
        precio = response.xpath('normalize-space(//div[@class="currentPrice"])').extract()[0]
        if precio[-1] == "\u20ac":
            precio = precio.replace("\u20ac", ".00 EUR")
        else:
            precio = precio.replace("\u20ac", ".") + ' EUR'
        tienda = [{
            'precio':precio,
            'nombre_tienda':'Conforama',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item