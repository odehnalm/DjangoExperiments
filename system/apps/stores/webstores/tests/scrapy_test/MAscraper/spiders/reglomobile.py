# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from FR_libs.MAscraper.MAscraper.items import MascraperItem

def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')

    if isinstance(raw_html,str):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    if isinstance(raw_html,list):
        cleantext = [re.sub(cleanr, '', componente) for componente in raw_html]
        return cleantext

class ReglomobileSpider(scrapy.Spider):
    name = 'reglomobile'
    allowed_domains = ['https://www.reglomobile.fr']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(ReglomobileSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):
        item = MascraperItem()
        nom_prod = response.xpath('//p[@class="nomAccrocheMobile"]//text()').extract()
        url_prod = response.xpath('//p[@class="nomAccrocheMobile"]/a/@href').extract()
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

        url_tienda = response.meta['url_tienda']

        #Ficha Tecnica
        specs = response.xpath('//td/span//text()').extract()
        ficha_tec={}
        for k in range(int(len(specs)/2)):
            ficha_tec[specs[2*k]] = specs[2*k+1]

        #Tienda
        precio = response.xpath('//span[@class="montantPrixMobile"]//text()').extract()[0].replace(',','.') + ' EUR'
        tienda = [{
            'precio':precio,
            'nombre_tienda':'Reglomobile',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = []
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item