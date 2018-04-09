import re

from scrapy import Request as ScrapyRequest

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    print(" -------------------------------------------  GET DATA METHOD")

    nom_prod = cleanhtml(response.xpath('//div[@class="prd-name"]').extract())
    print(nom_prod)
    availability = cleanhtml(response.xpath('//div[contains(@class,"sale_container")]/div[@class="sale_price"]').extract())
    print(availability)



    detail_prod = response.xpath('//ul[@class="infos_strenghts"]').extract()
    url_prod = response.xpath('//div[@class="prd-name"]/a/@href').extract()

    #Veamos si el producto está agotado
    try:
        #Arreglo que almacena indice de productos agotados
        items_to_pop = []
        for i in range(len(nom_prod)):
            if availability[i] == "\r\n": items_to_pop.append(i)
        #Eliminamos productos agotados
        for unavailable in items_to_pop: 
            nom_prod.pop(unavailable)
            detail_prod.pop(unavailable)
            url_prod.pop(unavailable)
    except:
        pass

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'https://www.darty.com'
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")

    item = response.meta['item']
    nom_prod = response.meta['nom_prod']
    detail_prod = response.meta['detail_prod']
    counter = response.meta['counter']
    url_tienda = 'https://www.darty.com' + response.meta['url_tienda']

    #Ficha Tecnica
    ficha_izq = cleanhtml(response.xpath('//table[contains(@class,"font-2")]/tbody/tr/th[descendant-or-self::text()]').extract())
    ficha_der = cleanhtml(response.xpath('//*[@id="product_caracteristics"]/div[2]/table/tbody/tr/td').extract())
    ficha_tec={}
    for k in range(len(ficha_der)):
        if ficha_der[k] == '&amp;nbsp':
            continue
        ficha_tec[ficha_izq[k]] = ficha_der[k]

    precio = response.xpath('normalize-space(//div[@class="product_price font-2-b"])').extract()[0].replace("\u20ac", "").replace(",", ".")

    if precio:

        #Tienda
        tienda = [{
            'precio': precio + " EUR",
            'nombre_tienda':'Darty', 'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['tiendas'] = tienda
        item['nombre'] = nom_prod[counter]
        item['detalles'] = cleanhtml(detail_prod[counter]).splitlines()[1:]
        item['ficha_tecnica'] = ficha_tec

    else:

        item['nombre'] = ""
        item['detalles'] = ""
        item['ficha_tecnica'] = ""
        item['tiendas'] = ""

    return item
