from scrapy import Request as ScrapyRequest

import re

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    print(" -------------------------------------------  GET DATA METHOD")

    start_url = kwargs.get('url', None)

    # Verificando existencia de resultados validos
    results_OK = response.xpath('//section[@class="selected-refinements"]').extract()

    if results_OK or start_url == 'http://www.kelkoo.fr/c-100311823-televiseur.html' or\
            start_url == 'http://www.kelkoo.fr/c-146401-refrigerateur.html' or\
            start_url == 'http://www.kelkoo.fr/c-100014413-cave-a-vin.html' or\
            start_url == 'http://www.kelkoo.fr/c-145701-congelateur.html' or\
            start_url == 'http://www.kelkoo.fr/c-145801-combine-refrigerateur-congelateur.html' or\
            start_url == 'http://www.kelkoo.fr/c-100020213-telephone-portable-sans-abonnement.html':

        nom_prod = response.xpath('//h3[@class="result-title"]').extract()
        url_prod = response.xpath(
            '//div[@class="result-link"]/@data-href').extract()

    else:
        nom_prod = []
        url_prod = []

    detail_prod = []

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'http://www.kelkoo.fr'
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")

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
    nom_tiendas = cleanhtml(response.xpath('//section[contains(@class,"od-main")]/div[contains(@class,"od-results")]//p[contains(@class,"merchant-name")]').extract())

    tiendas = []
    for k in range(len(nom_tiendas)):

        precio = response.xpath('normalize-space((//section[contains(@class,"od-main")]/div[contains(@class,"od-results")]//p[contains(@class,"price")]/strong)[{0}])'.format(k+1)).extract()[0].replace("\u20ac", "EUR").replace(',','.')

        tiendas.append({
            'precio' : precio,
            'nombre_tienda' : nom_tiendas[k].replace('\xa0',''),
            'url_tienda' : response.xpath('(//section[contains(@class,"od-main")]/div[contains(@class,"od-results")]//a[@class="result-link"]/@href)[{0}]'.format(k+1)).extract()[0]
        })

    # Guardamos la Informacion
    item['nombre'] = re.sub(
        '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
    )
    item['detalles'] = detail_prod
    item['ficha_tecnica'] = fiche_tec
    item['tiendas'] = tiendas

    return item

