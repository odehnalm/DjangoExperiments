# -*- coding: utf-8 -*-
import re

import scrapy

from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml

class ElectrodepotSpider(scrapy.Spider):
    name = 'electrodepot'
    allowed_domains = ['www.electrodepot.fr']

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(ElectrodepotSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        nom_prod_xpath = response.xpath('//span[contains(@class, "product-item-titre")]')
        url_prod = response.xpath(
            '//div[contains(@class, "product-info")]/a/@href').extract()

        n = len(nom_prod_xpath)

        for i in range(n):

            if i >= self.max_items:
                return

            nom_prod = nom_prod_xpath[i].xpath('normalize-space(text())')[0].extract()

            yield scrapy.Request(
                url_prod[i],
                callback=self.parse_individual,
                meta={'item': item, 'nom_prod': nom_prod,
                      'url_tienda': url_prod[i]},
                dont_filter=True
            )

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']

        # Detalles
        details_xpath = '//div[contains(@class, "product-keys")]/p[@itemprop="description"]/text()'
        details = response.xpath(details_xpath)

        details_count_xpath = 'count(' + details_xpath + ')'
        details_count = int(float(
            response.xpath(details_count_xpath).extract()[0]
        ))

        detail_prod = []
        for k in range(details_count):

            detail_parts = details[k].extract().split(":")
            detail_key = " ".join(re.findall(r"[\w']+", detail_parts[0]))
            detail_value = " ".join(re.findall(r"[\w']+", detail_parts[1]))
            detail = detail_key + " : " + detail_value
            detail_prod.append(detail)

        # Ficha Tecnica
        xpath_keys = "//td[contains(@class, 'titre')]"
        xpath_values = "//td[contains(@class, 'valeur')]"
        fiche_tec_keys = cleanhtml(response.xpath(xpath_keys).extract())
        fiche_tec_values = cleanhtml(response.xpath(xpath_values).extract())

        fiche_tec = {}
        for k in range(len(fiche_tec_keys)):
            fiche_tec[fiche_tec_keys[k]] = fiche_tec_values[k]

        # Tienda
        url_tienda = response.meta['url_tienda']
        xpath_price = '//span[contains(@class, "price-container")]//span[contains(@class, "price-wrapper")]/@data-price-amount'
        precio = response.xpath(xpath_price).extract()[0]

        tienda =[ {
            'precio': precio + " EUR",
            'nombre_tienda': 'Electrodepot',
            'url_tienda': url_tienda
        }]

        # Guardamos la Informacion
        item['nombre'] = re.sub(
            '  +', '', cleanhtml(nom_prod).replace('\n', '')
        )
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = fiche_tec
        item['tiendas'] = tienda

        yield item
