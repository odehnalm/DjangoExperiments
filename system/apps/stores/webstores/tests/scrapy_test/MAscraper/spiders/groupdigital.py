# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider
from MAscraper.items import MascraperItem
from MAscraper.utils.html import cleanhtml

class GroupDigitalSpider(scrapy.Spider):
    name = 'groupdigital'
    allowed_domains = ['www.group-digital.fr']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(GroupDigitalSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        nom_model = cleanhtml(response.xpath('//p[@class="product-sku"]').extract())
        nom_prod = []
        for i in range(len(nom_model)):
            nom_prod.append(response.xpath('normalize-space((//span[@class="supplierref"])[{0}])'.format(i+1)).extract()[0].replace('\xa0',' - ') + nom_model[i] + nom_model[i])

        nom_marque = []

        url_prod = response.xpath('//h2/a/@href').extract()
        n = len(nom_prod)

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

        # Detalles
        detalles = cleanhtml(response.xpath('//div[@class="std"]/ul/li').extract())

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//tbody/tr/th').extract())
        ficha_der = cleanhtml(response.xpath('//tbody/tr/td').extract())
        ficha_tec={}
        for k in range(len(ficha_der)):
            if ficha_der[k] == '&amp;nbsp':
                continue
            ficha_tec[ficha_izq[k]] = ficha_der[k]

        xpath_regular = 'normalize-space(//div[@class="inside-col-right-content"]//span[@class="regular-price"])'
        xpath_oferta = 'normalize-space(//div[@class="inside-col-right-content"]//p[@class="special-price"]/span[@class="price"])'

        #Caso ofertas primero
        precio = response.xpath(xpath_oferta).extract()[0].replace('\xa0','').replace("\u20ac", "").replace(' ','').replace(",", ".")

        #Caso regular despues
        if precio == '':
            precio = response.xpath(xpath_regular).extract()[0].replace('\xa0','').replace("\u20ac", "").replace(' ','').replace(",", ".")

        if precio:

            tienda = [{
                'precio': precio + " EUR",
                'nombre_tienda':'Group Digital', 'url_tienda': url_tienda }]

            #Guardamos la Informacion
            item['tiendas'] = tienda
            item['nombre'] = nom_prod[counter]
            item['detalles'] = detalles
            item['ficha_tecnica'] = ficha_tec

        else:

            item['nombre'] = ""
            item['detalles'] = ""
            item['ficha_tecnica'] = ""
            item['tiendas'] = ""

        yield item