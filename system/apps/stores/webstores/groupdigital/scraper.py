from scrapy import Request as ScrapyRequest

import re

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    nom_model = cleanhtml(response.xpath('//p[@class="product-sku"]').extract())
    nom_prod = []
    for i in range(len(nom_model)):
        nom_prod.append(response.xpath('normalize-space((//span[@class="supplierref"])[{0}])'.format(i+1)).extract()[0].replace('\xa0',' - ') + nom_model[i])

    nom_marque = []
    detail_prod = []

    url_prod = response.xpath('//h2/a/@href').extract()

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': ''
    }


def get_item_data(response):

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

    return item
