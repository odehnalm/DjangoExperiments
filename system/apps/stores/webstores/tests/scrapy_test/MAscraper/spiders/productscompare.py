# -*- coding: utf-8 -*-
import re
import scrapy
from MAscraper.items import MascraperItem
from MAscraper.utils.html import cleanhtml


class ProductsCompareSpider(scrapy.Spider):
    name = 'products-compare'
    allowed_domains = ['http://www.electromenager-compare.com','http://www.lcd-compare.com']

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(ProductsCompareSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        print('entre')
        item = MascraperItem()
        nom_prod = response.xpath('//div[@class="product-list"]/div/div[@class="product-list-info"]/a/text()').extract()
        url_prod = response.xpath(
            '//div[@class="product-list"]/div/div[@class="product-list-info"]/a/@href').extract()
        print(nom_prod)
        print(url_prod)

        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                return

            yield scrapy.Request(
                '' + url_prod[i],
                callback=self.parse_individual,
                meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                      'url_tienda': url_prod[i]},
                dont_filter=True
            )

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        comparador = response.meta['url_tienda'].split('.com/')[0] + '.com/' 
        counter = response.meta['counter']

        # Detalles
        detail_prod = response.xpath('//div[@class="product-specs"]/ul/li').extract()
        for i in range(len(detail_prod)):
            detail_prod[i] = cleanhtml(detail_prod[i])
        
        # Ficha Tecnica
        xpath_keys = "//div[@class='product-tech-section-row']/div[1]"
        xpath_values = "//div[@class='product-tech-section-row']/div[2]"
        fiche_tec_keys = cleanhtml(response.xpath(xpath_keys).extract())
        fiche_tec_values = cleanhtml(response.xpath(xpath_values).extract())
        #
        fiche_tec = {}
        for k in range(len(fiche_tec_keys)):
            fiche_tec[fiche_tec_keys[k].replace('\n','').replace('\r','').replace('\t','').replace('• ','').replace(' :','')] =\
             fiche_tec_values[k].replace('\n','').replace('\r','').replace('\t','')
        
        nom_tiendas = cleanhtml(response.xpath('//div[@class="product-prices-list-row-retailer"]/a[2]').extract())
        
        #Tiendas
        tiendas = []
        for k in range(len(nom_tiendas)):
            if "chez" in nom_tiendas[k]: nom_tiendas[k] = nom_tiendas[k].split(" chez ")[1]
            tiendas.append({
                'precio' : response.xpath('normalize-space((//div[@class="product-prices-list-row-price-details"]/div/a[contains(@class,"tip-ajax")])[{0}])'.format(k+1)).extract()[0]
                  .replace("\u20ac", "EUR").replace(',','.').replace('\xa0',' '),
                'nombre_tienda' : nom_tiendas[k].replace('\xa0','').replace('\r','').replace('\n',''),
                'url_tienda' : comparador  + response.xpath('(//div[@class="product-prices-list-row-retailer"]/a[2]/@href)[{0}]'.format(k+1)).extract()[0]
            })
        
        # Guardamos la Informacion
        item['nombre'] = re.sub(
            '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
        )
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = fiche_tec
        item['tiendas'] = tiendas

        yield item
