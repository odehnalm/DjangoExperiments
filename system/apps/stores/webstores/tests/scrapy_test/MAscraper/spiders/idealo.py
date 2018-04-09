# -*- coding: utf-8 -*-
import re
import scrapy
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml


class IdealoSpider(scrapy.Spider):
    name = 'idealo'
    allowed_domains = ['www.idealo.fr']
    start_urls = [
        'http://www.idealo.fr/cat/2800/refrigerateurs.html'
    ]

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def parse(self, response):

        item = MascraperItem()

        nom_prod = response.xpath('//h3[@class="result-title"]').extract()
        url_prod = response.xpath(
            '//div[@class="result-link"]/@data-href').extract()
        n = len(nom_prod)

        for i in range(n):

            if i >= self.max_items:
                return

            yield scrapy.Request(
                'http://www.kelkoo.fr' + url_prod[i],
                callback=self.parse_individual,
                meta={'item': item, 'nom_prod': nom_prod, 'counter': i,
                      'url_tienda': url_prod[i]},
                dont_filter=True
            )

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        # Detalles
        detail_count_xpath = 'count(//ul[@class="top-attributes"]/li)'
        detail_count = int(float(
            response.xpath(detail_count_xpath).extract()[0]
        ))

        detail_prod = []
        for k in range(detail_count):
            detail_xpath = '//ul[@class="top-attributes"]/li[' + str(k + 1) + ']'
            detail_prod.append(
                response.xpath('normalize-space(' + detail_xpath + ')').extract()[0]
            )

        # Ficha Tecnica
        xpath_keys = "//section[@id='product-info']//dl[@class='specification-block']/dt"
        xpath_values = "//section[@id='product-info']//dl[@class='specification-block']/dd"
        fiche_tec_keys = cleanhtml(response.xpath(xpath_keys).extract())
        fiche_tec_values = cleanhtml(response.xpath(xpath_values).extract())

        fiche_tec = {}
        for k in range(len(fiche_tec_keys)):
            fiche_tec[fiche_tec_keys[k]] = fiche_tec_values[k]

        # Tienda
        url_tienda = 'http://www.kelkoo.fr' + response.meta['url_tienda']
        xpath_price = '//span[@itemprop="lowprice"]/text()'
        precio = response.xpath(xpath_price).extract()[0]

        tienda = [{
            'precio': precio + " EUR",
            'nombre_tienda': 'Kelkoo',
            'url_tienda': url_tienda
        }]

        # Guardamos la Informacion
        item['nombre'] = re.sub(
            '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
        )
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = fiche_tec
        item['tiendas'] = tienda

        yield item
