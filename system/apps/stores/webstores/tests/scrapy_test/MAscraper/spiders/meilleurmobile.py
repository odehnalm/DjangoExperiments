# -*- coding: utf-8 -*-
import re
import scrapy
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml


class MeilleurMobileSpider(scrapy.Spider):
    name = 'meilleurmobile'
    allowed_domains = ['www.meilleurmobile.com']

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(MeilleurMobileSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        number_item = int(float(response.xpath('count(//span[@class="produit_desc_txt"])').extract()[0]))
        nom_prod = []
        for k in range(number_item):
            xpath_nom = 'normalize-space((//span[@class="produit_desc_txt"])['+str(k+1)+'])'
            nom_prod.append(response.xpath(xpath_nom).extract()[0])
        url_prod = response.xpath(
            '//h2/a/@href').extract()
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                return

            tiendaname_xpath = '(//ul[@class="caracPrincipales seul productType1"])[1]/li[@class="clearer listOperateurs"]/a/span[1]/span/img/@alt'
            tiendaname_xpath = '(//ul[@class="caracPrincipales seul productType1"])[1]/li'
            print(response.xpath(tiendaname_xpath).extract())

            yield scrapy.Request(
                'http://www.meilleurmobile.com' + url_prod[i],
                callback=self.parse_individual,
                meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                      'url_tienda': url_prod[i]},
                dont_filter=True
            )

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']
        url_tienda = response.meta['url_tienda']

        # Detalles
        detail_prod = response.xpath('//ul[@class="caracPrincipales"]/li//text()').extract()

        # Ficha Tecnica
        xpath_keys = "//li/label"
        xpath_values = 'normalize-space((//li/div[@class="topic"])[{0}])'
        fiche_tec_keys = cleanhtml(response.xpath(xpath_keys).extract())

        fiche_tec = {}
        for k in range(len(fiche_tec_keys)):
            fiche_tec[fiche_tec_keys[k]] = response.xpath(xpath_values.format(k+1)).extract()[0]

        # URL DE LAS OFERTAS
        phoneid = url_tienda.split('_')[-1].split('.')[0]
        url_ofertas = 'https://www.meilleurmobile.com/forfaits/priceByOperator.do?mobileId=' + phoneid


        item['nombre'] = re.sub(
            '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
        )
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = fiche_tec
        #item['tiendas'] = tiendas

        yield item

