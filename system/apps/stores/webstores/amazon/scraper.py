import re

from scrapy import Request as ScrapyRequest

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    print(" -------------------------------------------  GET DATA METHOD")

    detail_prod = []
    number_item = int(float(response.xpath('count(//li[contains(@id,"result")]/div/div[3]/div[1]/a/h2)').extract()[0]))
    nom_prod = []
    for k in range(number_item):
        xpath_nom = 'normalize-space((//li[contains(@id,"result")]/div/div[3]/div[1]/a/h2)['+str(k+1)+'])'
        nom_prod.append(response.xpath(xpath_nom).extract()[0])

    url_prod = response.xpath('//li[contains(@id,"result")]/div/div[3]/div[1]/a/@href').extract()

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': ''
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")

    item = response.meta['item']
    nom_prod = response.meta['nom_prod']
    counter = response.meta['counter']

    #Detalles
    detail_count = int(float(response.xpath('count(//div[@id="productDescription" and @class="a-section a-spacing-small"]/p/br)').extract()[0]))

    #Caso parrafo
    if detail_count == 0:
        detail_prod = [cleanhtml(response.xpath('normalize-space(//div[@id="productDescription" and @class="a-section a-spacing-small"])').extract()[0])]
    #Caso lista
    else:
        # print(cleanhtml(response.xpath('//div[@id="productDescription" and @class="a-section a-spacing-small"]/p').extract()[0].split('<br>')))
        detail_prod = cleanhtml(response.xpath('//div[@id="productDescription" and @class="a-section a-spacing-small"]/p').extract()[0].split('<br>'))


    url_tienda = response.meta['url_tienda']

    #Ficha Tecnica
    ficha_izq = cleanhtml(response.xpath('//tbody/tr/td[@class="label"]').extract())
    ficha_der = cleanhtml(response.xpath('////tbody/tr/td[@class="value"]').extract())
    ficha_tec={}
    for k in range(len(ficha_izq)):
        try:
            if ficha_izq[k][-4:]=='Aide':
                ficha_izq[k]=ficha_izq[k][:-4]
                ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0','')
            else:
                ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')
        except:
            ficha_tec[ficha_izq[k].replace('\xa0','')] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')

    #Tienda
    precio = response.xpath('normalize-space(//span[@id="priceblock_ourprice"])').extract()[0].replace('\xa0','').replace('EUR ','').replace(' ','').replace(',','.')

    if precio:

        tienda = [{
            'precio': precio + ' EUR',
            'nombre_tienda':'Amazon',
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

