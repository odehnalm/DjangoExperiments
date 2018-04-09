# -*- coding: utf-8 -*-
import scrapy
from MAscraper.items import MascraperItem
from MAscraper.utils.html import cleanhtml

class BoulangerSpider(scrapy.Spider):

    name = 'boulanger'
    allowed_domains = ['www.boulanger.com']

    #Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(BoulangerSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        number_item = int(float(response.xpath('count(//div[@class="designations"]/h2)').extract()[0]))
        nom_prod = []
        for k in range(number_item):
            xpath_nom = 'normalize-space((//div[@class="designations"]/h2)['+str(k+1)+'])'
            nom_prod.append(response.xpath(xpath_nom).extract()[0])

        url_prod = response.xpath('//div[@class="designations"]/h2/a/@href').extract()
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                print(i)
                return
                #raise CloseSpider('bandwidth_exceeded')

            yield scrapy.Request('https://www.boulanger.com' + url_prod[i], callback=self.parse_individual,
                                 meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                                       'url_tienda':url_prod[i]},dont_filter=True)

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        #Detalles
        detail_count = int(float(response.xpath('count(//li[@class="bestpoint"])').extract()[0]))
        detail_prod = []
        for k in range(detail_count):
            detail_xpath = '//li[@class="bestpoint"][' +str(k+1)+ ']'
            detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])



        url_tienda = 'https://www.boulanger.com' + response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//table[@class="characteristic"]/tbody/tr/td/span/text()[1][normalize-space()]').extract())
        ficha_der = cleanhtml(response.xpath('//table[@class="characteristic"]/tbody/tr/td/text()').extract())
        print(ficha_izq)
        ficha_tec={}
        for k in range(len(ficha_izq)):
            print(ficha_izq[k])
            try:
                if ficha_izq[k][-4:]=='Aide':
                    ficha_izq[k]=ficha_izq[k][:-4]
                    ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r', '').replace('\t', '').replace('\n', '')
                else:
                    ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','')
            except:
                print(ficha_izq[k])
                ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','')

        #Tienda
        tienda = [{
            'precio': response.xpath('normalize-space(//span[contains(@class,"StrikeoutPrice")])').extract()[0].split(' ')[0].
                          replace("\u20ac", ".") + ' EUR',
            'nombre_tienda':'Boulanger',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item