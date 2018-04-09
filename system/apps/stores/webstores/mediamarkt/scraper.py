from scrapy import Request as ScrapyRequest

import re

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    nom_prod = cleanhtml(response.xpath('//div[@class="product10Description"]/h2/a').extract())
    url_prod = cleanhtml(response.xpath('//div[@class="product10Description"]/h2/a/@href').extract())
    detail_prod = cleanhtml(response.xpath('//div[@class="product10ShortDescription"]//text()').extract())

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'https://tiendas.mediamarkt.es'
    }


def get_item_data(response):

    item = response.meta['item']

    nom_prod = response.meta['nom_prod']
    detalles = response.meta['detail_prod']
    counter = response.meta['counter']
    url_tienda = "https://tiendas.mediamarkt.es" + response.meta['url_tienda']

    #Ficha Tecnica
    ficha_izq = cleanhtml(response.xpath('//div[@class="customTagName productCustomTagName"]//text()').extract())
    ficha_izq = [x.replace('\n','') for x in ficha_izq if x != '\n']
    ficha_der = cleanhtml(response.xpath('//div[@class="customTagValue productCustomTagValue"]').extract())
    ficha_der = [x.replace('\n', '')[:-1] for x in ficha_der if x!= '\n']
    ficha_tec={}
    for k in range(len(ficha_der)):
        ficha_tec[ficha_izq[k]] = ficha_der[k]

    precio = cleanhtml(response.xpath('//div[@id="priceBlock"]/div').extract()[0]).replace(',','.').replace(' ','')

    if precio:

        #Tienda
        tienda = [{
            'precio': precio + ' EUR',
            'nombre_tienda':'MediaMarkt', 'url_tienda': url_tienda }]

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
