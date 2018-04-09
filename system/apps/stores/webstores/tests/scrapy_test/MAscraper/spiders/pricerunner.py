# -*- coding: utf-8 -*-
import json
import re

from lxml import html
import scrapy
from scrapy_splash import SplashRequest

from MAscraper.items import MascraperItem
from MAscraper.utils.html import cleanhtml


class PricerunnerSpider(scrapy.Spider):
    name = 'pricerunner'
    allowed_domains = ['www.pricerunner.fr']

    def __init__(self, *args, **kwargs):
        super(PricerunnerSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):

        urls = self.start_urls

        for url_pr in urls:

            category_num = url_pr.replace("http://www.pricerunner.fr/cl/", "").split('/')[0]

            filtros_pr = url_pr.split('#')[1].replace('sort=3', 'cat=' + category_num + '&sort=3')

            referer_pr = url_pr.split('#')[0]

            if "man_id=" in referer_pr:
                man_id = referer_pr.split("?")[1] + "&"
            else:
                man_id = ""

            url = "http://www.pricerunner.fr/mod_shopping/public/product-list?" + man_id + filtros_pr + "&viewType=standard&loadGuide=1"

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7',
                'Connection': 'keep-alive',
                'Cookie': '',
                'Host': 'www.pricerunner.fr',
                'Referer': referer_pr,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            yield scrapy.Request(
                url,
                meta={
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302]
                },
                headers=headers,
                callback=self.parse,
                dont_filter=True)

        # yield SplashRequest(self.start_urls[0],
        #                      self.parse,
        #                          args={
        #                          # optional; parameters passed to Splash HTTP API
        #                          'wait': 25.5,
        #                          # 'url' is prefilled from request url
        #                          # 'http_method' is set to 'POST' for POST requests
        #                          # 'body' is set to request body for POST requests
        #                      },
        #                      meta={
        #                          'dont_redirect': True,
        #                          'handle_httpstatus_list': [302]
        #                      },
        #                      dont_filter=True)

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def parse(self, response):

        jsonresponse = json.loads(response.body_as_unicode())
        html_response = html.fromstring(jsonresponse['list'])

        item = MascraperItem()
        nom_prod = html_response.xpath(
            '//div[@class="productname"]//a/text()')
        url_prod = html_response.xpath(
            '//p[@class="productdescription"]/a/@href')

        n = len(nom_prod)
        for i in range(n):

            if i >= self.max_items:
                return

            yield scrapy.Request(
                'http://www.pricerunner.fr' + url_prod[i],
                callback=self.parse_individual,
                meta={
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302],
                    'item': item, 'nom_prod': nom_prod, 'counter': i,
                    'url_tienda': url_prod[i]},
                dont_filter=True
            )

    def parse_individual(self, response):

        item = response.meta['item']
        nom_prod = response.meta['nom_prod']
        counter = response.meta['counter']

        # Detalles
        detail_xpath = 'normalize-space(//div[contains(@class, "productinfocontent")]//dd[contains(@class, "description_col")]/p/a/text())'
        detail_prod = response.xpath(detail_xpath).extract()[0].split(", ")


        # Ficha Tecnica
        #xpath_keys = "//div[contains(@class, 'product-specs')]//tbody/tr[position()>1]/th"
        #xpath_values = "//div[contains(@class, 'product-specs')]//tbody/tr[position()>1]/td"
        #fiche_tec_keys_len = response.xpath("count(//div[contains(@class, 'product-specs')]//tbody/tr[not(contains (@class, 'heading'))]/th)").extract()[0]
        fiche_tec_values_len = response.xpath("count(//div[contains(@class, 'product-specs')]//tbody/tr[not(contains (@class, 'heading'))]/td)").extract()[0]
        #fiche_tec_izq = []
        #fiche_tec_der = []




        # #limpieza de vacios
        #fiche_tec_izq = [x for x in fiche_tec_izq if x]
        #fiche_tec_der = [x for x in fiche_tec_der if x]
        #
        fiche_tec = {}

        for k in range(int(float(fiche_tec_values_len))):
            fiche_tec_izq = cleanhtml(response.xpath(
                "normalize-space((//div[contains(@class, 'product-specs')]//tbody/tr[not(contains (@class, 'heading'))]/th)[{0}])".format(
                    k + 1)).extract()[0])
            fiche_tec_der = cleanhtml(response.xpath(
                "normalize-space((//div[contains(@class, 'product-specs')]//tbody/tr[not(contains (@class, 'heading'))]/td)[{0}])".format(
                    k + 1)).extract()[0])
            fiche_tec[fiche_tec_izq] = fiche_tec_der
        #     key = cleanhtml(fiche_tec_keys[k].xpath('normalize-space(text())')[0].extract())
        #     value = cleanhtml(fiche_tec_values[k].xpath('normalize-space(text())')[0].extract())
        #     text_from_a = cleanhtml(fiche_tec_values[k].xpath('a/text()').extract())
        #
        #     if text_from_a:
        #         value = text_from_a[0]
        #
        #     fiche_tec_izq.append[key] = value

        # Tiendas

        url_tienda = 'http://www.pricerunner.fr' + response.meta['url_tienda']
        url_ofertas = url_tienda.replace('/pi/','/pli/').replace('informations-produit','comparer-les-prix')
        print(url_ofertas)

        #xpath_price = "translate(normalize-space(//a[contains(@class, 'price-range')]/strong), ' ', '')"
        #precio = response.xpath(xpath_price).extract()[0].replace("\u20ac", " EUR").replace(',', '.')

        # Guardamos la Informacion
        nombre = re.sub(
            '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
        )
        detalles = detail_prod

        yield scrapy.Request(
            url_ofertas,
            callback=self.parse_ofertas,
            meta={                                 'dont_redirect': True,
                                 'handle_httpstatus_list': [302],'item': item,'nombre':nombre,'detalles':detail_prod,'ficha_tec':fiche_tec},
            dont_filter=True
        )

    def parse_ofertas(self,response):

        item = response.meta['item']
        item['nombre'] = response.meta['nombre']
        item['detalles'] = response.meta['detalles']
        item['ficha_tecnica'] = response.meta['ficha_tec']

        nom_tiendas = response.xpath('//h4/a/@retailer-data').extract()

        tiendas = []
        for k in range(len(nom_tiendas)):
            tiendas.append({
                'precio' : response.xpath('normalize-space((//div[@class="price-content"])[{0}])'.format(k+1)).extract()[0].split(' excl. ')[0]
                  .replace("\u20ac", " EUR").replace(',','.'),
                'nombre_tienda' : nom_tiendas[k].split('(')[0].replace('\xa0',''),
                'url_tienda' : 'http://www.pricerunner.fr' + response.xpath('(//h4/a/@href)[{0}]'.format(k+1)).extract()[0]
            })

        item['tiendas'] = tiendas

        yield item
