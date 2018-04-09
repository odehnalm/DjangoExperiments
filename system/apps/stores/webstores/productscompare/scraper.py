from scrapy import Request as ScrapyRequest

import re

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    nom_prod = response.xpath('//div[@class="product-list"]/div/div[@class="product-list-info"]/a/text()').extract()
    url_prod = response.xpath(
        '//div[@class="product-list"]/div/div[@class="product-list-info"]/a/@href').extract()

    return {
        'nom_prod': nom_prod,
        'url_prod': url_prod,
        'detail_prod' : [],
        'url_base': ''
    }


def get_item_data(response):

    item = response.meta['item']
    nom_prod = response.meta['nom_prod']
    comparador = response.meta['url_tienda'].split('.com/')[0] + '.com/' 
    counter = response.meta['counter']

    # Detalles
    detail_prod = response.xpath('//div[@class="product-specs"]/ul/li').extract()
    for i in range(len(detail_prod)):
        detail_prod[i] = cleanhtml(detail_prod[i])

    # Ficha Tecnica
    xpath_keys = "//div[@class='product-tech-section-row']/div[1]"
    xpath_values = "//div[@class='product-tech-section-row']/div[2]"
    fiche_tec_keys = cleanhtml(response.xpath(xpath_keys).extract())
    fiche_tec_values = cleanhtml(response.xpath(xpath_values).extract())
    #
    fiche_tec = {}
    for k in range(len(fiche_tec_keys)):
        fiche_tec[fiche_tec_keys[k].replace('\n','').replace('\r','').replace('\t','').replace('• ','').replace(' :','')] =\
         fiche_tec_values[k].replace('\n','').replace('\r','').replace('\t','')
    
    nom_tiendas = cleanhtml(response.xpath('//div[@class="product-prices-list-row-retailer"]/a[2]').extract())
    
    #Tiendas
    tiendas = []
    for k in range(len(nom_tiendas)):
        if "chez" in nom_tiendas[k]: nom_tiendas[k] = nom_tiendas[k].split(" chez ")[1]

        precio = response.xpath('normalize-space((//div[@class="product-prices-list-row-price-details"]/div/a[contains(@class,"tip-ajax")])[{0}])'.format(k+1)).extract()[0].replace("\u20ac", "").replace(',','.').replace('\xa0', '').replace(' ','')

        if precio:

            tiendas.append({
                'precio': precio + " EUR",
                'nombre_tienda': nom_tiendas[k].replace('\xa0','').replace('\r','').replace('\n',''),
                'url_tienda': comparador + response.xpath('(//div[@class="product-prices-list-row-retailer"]/a[2]/@href)[{0}]'.format(k+1)).extract()[0]
            })

    if tiendas:
        # Guardamos la Informacion
        item['nombre'] = re.sub(
            '  +', '', cleanhtml(nom_prod[counter]).replace('\n', '')
        )
        item['detalles'] = detail_prod
        item['ficha_tecnica'] = fiche_tec
        item['tiendas'] = tiendas
    else:
        item['nombre'] = ""
        item['detalles'] = ""
        item['ficha_tecnica'] = ""
        item['tiendas'] = ""

    return item
