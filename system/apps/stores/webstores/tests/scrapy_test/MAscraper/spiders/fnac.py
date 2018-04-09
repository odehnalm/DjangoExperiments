# -*- coding: utf-8 -*-
import re
import scrapy
from FR_libs.MAscraper.MAscraper.items import MascraperItem
from FR_libs.MAscraper.MAscraper.utils.html import cleanhtml


class FnacSpider(scrapy.Spider):
    name = 'fnac'
    allowed_domains = ['www.fnac.com']

    # Max items y Rotate Agent
    max_items = 5
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(FnacSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls')
        if not urls:
            raise ValueError('No urls given')

        self.start_urls = urls

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],callback=self.parse,dont_filter=True)

    def parse(self, response):

        item = MascraperItem()
        nom_prod_xpath = response.xpath('//div[contains(@class, "Article-itemInfo")]//p[@class="Article-desc"]/a/text()')
        url_prod = response.xpath(
            '//div[contains(@class, "Article-itemInfo")]//p[@class="Article-desc"]/a/@href').extract()

        n = len(nom_prod_xpath)

        for i in range(n):

            if i >= self.max_items:
                return

            nom_prod = nom_prod_xpath[i].extract()

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

        type_produit = 'mobiles'


        if type_produit == 'froid':

            # ---- Detalles
            details_xpath = '//div[contains(@class, "js-productSummaryTrimHeight-target")]//text()'
            details_list = response.xpath(details_xpath).extract()

            # Busqueda de subtitulo separador de lista de detalles a ficha tecnica
            try:
                index_subtitle = details_list.index("Caractéristiques Techniques")
                details_parts = details_list[:index_subtitle]
                fiche_tec_list = details_list[index_subtitle + 1:]

                detect_items = list(
                    map(lambda x: x.startswith('- '), details_parts)
                )
                if True in detect_items:
                    details_parts = details_parts[detect_items.index(True):]
                    detail_prod = list(
                        map(lambda x: x[2:].translate(
                            str.maketrans("\n\r\t", "   ")).strip(), details_parts)
                    )

                detect_items = list(
                    map(lambda x: x.startswith('- '), fiche_tec_list)
                )

                if True in detect_items:
                    fiche_tec_list = fiche_tec_list[detect_items.index(True):]
                    fiche_tec_list = list(
                        map(lambda x: x[2:].translate(
                            str.maketrans("\n\r\t", "   ")).strip(), fiche_tec_list)
                    )

                else:
                    details_str = " ".join(details_list)
                    details_str = details_str.translate(str.maketrans("\n\r\t", "   "))
                    detail_prod = [details_str.strip()]

            except ValueError:
                # No existe tal separador, por lo que todo el contenido
                # es un listado de detalles a manera de resumen

                fiche_tec_list = []
                details_str = " ".join(details_list)
                details_str = details_str.translate(str.maketrans("\n\r\t", "   "))
                detail_prod = [details_str.strip()]

            # Ficha Tecnica
            fiche_tec_list = list(filter(None, fiche_tec_list))
            fiche_tec = {}
            for elem in fiche_tec_list:
                elem_list = elem.split(":")
                fiche_tec[elem_list[0]] = elem_list[1]

        elif type_produit == 'mobiles':

            #Detalles
            detail_prod = []
            detail_prod_izq = cleanhtml(response.xpath('//span[@class="f-productDetails-cellValue"]').extract())
            detail_prod_der = cleanhtml(response.xpath('//b[@class="f-productDetails-cellValue"]').extract())
            for k in range(len(detail_prod_izq)):
                detail_prod.append(detail_prod_izq[k] + ' : ' + detail_prod_der[k])

            #Ficha Tecnica
            fiche_tec = {}
            fiche_tec_izq = cleanhtml(response.xpath('//span[@class="Feature-label"]/span').extract())
            fiche_tec_der = cleanhtml(response.xpath('//span[@class="Feature-desc"]/span').extract())
            for k in range(len(fiche_tec_izq)):
                fiche_tec[fiche_tec_izq[k]] = fiche_tec_der[k]


        #Ficha Tecnica

        # Tienda
        url_tienda = response.meta['url_tienda']
        xpath_price = '//div[contains(@class, "f-priceBox")]/span/text()'
        xpath_subprice = '//div[contains(@class, "f-priceBox")]/span/sup/text()'
        precio = response.xpath(xpath_price).extract()[0].replace("\u20ac", "")
        subprecio = response.xpath(xpath_subprice).extract()

        if subprecio:
            precio = precio + '.' + subprecio[0].replace("\u20ac", "")

        tienda = [{
            'precio': precio + " EUR",
            'nombre_tienda': 'FNAC',
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
