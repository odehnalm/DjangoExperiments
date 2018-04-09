import re

from scrapy import Request as ScrapyRequest

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml
from ...utils import html2list


def get_data(response, **kwargs):

    print(" -------------------------------------------  GET DATA METHOD")

    number_item = int(float(response.xpath('count(//div[@class="summary"]/h2)').extract()[0]))
    nom_prod = []
    for k in range(number_item):
        xpath_nom = 'normalize-space((//div[@class="summary"]/h2)['+str(k+1)+'])'
        nom_prod.append(response.xpath(xpath_nom).extract()[0])

    url_prod = response.xpath('//article/a/@href').extract()

    detail_prod = []

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'https://www.rueducommerce.fr'
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")


    item = response.meta['item']
    nom_prod = response.meta['nom_prod']
    counter = response.meta['counter']

    #Detalles
    detalles = html2list(response.xpath('//div[@class="flexGrid-box boxCol2 noPadding tab-desc"]')
                         .extract()[0].replace('\xa0',' ')).splitlines()
    detail_prod = [x for x in detalles if x != ''][2:]

    url_tienda = 'https://www.rueducommerce.fr' + response.meta['url_tienda']

    #Ficha Tecnica
    num_fictec = int(float(response.xpath('count(//table[@id="blocAttributesContent"]/tbody/tr/td)').extract()[0])/2)
    ficha_tec={}
    for k in range(num_fictec):
        ficha_tec[response.xpath('normalize-space((//table[@id="blocAttributesContent"]/tbody/tr/td)['+str(2*k+1)+'])').extract()[0].replace('\xa0:','')] = \
            response.xpath('normalize-space((//table[@id="blocAttributesContent"]/tbody/tr/td)[' + str(2*k+2) + '])').extract()[0]

    #Tienda
    precio = response.xpath('normalize-space((//div[@class="price main"])[2])').extract()[0].replace("\u20ac", ".").replace('\xa0', '').replace(" ", "")
    
    if precio:

        tienda = [{
            'precio':precio + ' EUR',
            'nombre_tienda':'Rue du commerce',
            'url_tienda': url_tienda }]

        #Guardamos la Informacion
        item['nombre'] = nom_prod[counter]
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = ficha_tec
        item['tiendas'] = tienda
    else:
        item['nombre'] = ""
        item['detalles'] = ""
        item['ficha_tecnica'] = ""
        item['tiendas'] = ""

    return item
