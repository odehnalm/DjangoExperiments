# -*- coding: utf-8 -*-
import scrapy
from MAscraper.items import MascraperItem
from MAscraper.utils.html import cleanhtml

class AmazonSpider(scrapy.Spider):

    name = 'amazon'
    allowed_domains = ['www.amazon.fr']

    #Max items y Rotate Agent
    max_items = 30
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        number_item = int(float(response.xpath('count(//li[contains(@id,"result")]/div/div[3]/div[1]/a/h2)').extract()[0]))
        nom_prod = []
        for k in range(number_item):
            xpath_nom = 'normalize-space((//li[contains(@id,"result")]/div/div[3]/div[1]/a/h2)['+str(k+1)+'])'
            nom_prod.append(response.xpath(xpath_nom).extract()[0])

        url_prod = response.xpath('//li[contains(@id,"result")]/div/div[3]/div[1]/a/@href').extract()
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                print(i)
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
        # Contamos a ver si tenemos lista de detalles o un parrafo

        detail_count = int(float(response.xpath('count(//div[@id="productDescription" and @class="a-section a-spacing-small"]/p/br)').extract()[0]))

        #Caso parrafo
        if detail_count == 0:
            detail_prod = [cleanhtml(response.xpath('normalize-space(//div[@id="productDescription" and @class="a-section a-spacing-small"])').extract()[0])]
        #Caso lista
        else:
            # print(cleanhtml(response.xpath('//div[@id="productDescription" and @class="a-section a-spacing-small"]/p').extract()[0].split('<br>')))
            detail_prod = cleanhtml(response.xpath('//div[@id="productDescription" and @class="a-section a-spacing-small"]/p').extract()[0].split('<br>'))
        
        # print('number of details:    '+ str(detail_count))
        # for k in range(detail_count):
        #     detail_xpath = '//li[@class="bestpoint"][' +str(k+1)+ ']'
        #     detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])



        url_tienda = '' + response.meta['url_tienda']

        #Ficha Tecnica
        ficha_izq = cleanhtml(response.xpath('//tbody/tr/td[@class="label"]').extract())
        ficha_der = cleanhtml(response.xpath('////tbody/tr/td[@class="value"]').extract())
        ficha_tec={}
        for k in range(len(ficha_izq)):
            try:
                if ficha_izq[k][-4:]=='Aide':
                    ficha_izq[k]=ficha_izq[k][:-4]
                    ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0','')
                else:
                    ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')
            except:
                ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')

        #Tienda
        tienda = [{
            'precio': response.xpath('normalize-space(//span[@id="priceblock_ourprice"])').extract()[0].replace('EUR ','').replace(',','.') + ' EUR',
            'nombre_tienda':'Amazon',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter].replace('\xa0','')
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda

        yield item