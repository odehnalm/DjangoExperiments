import re

from scrapy import Request as ScrapyRequest

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def get_data(response, **kwargs):

    print(" -------------------------------------------  GET DATA METHOD")

    detail_prod = []
    number_item = int(float(response.xpath('count(//div[@class="designations"]/h2)').extract()[0]))
    nom_prod = []
    for k in range(number_item):
        xpath_nom = 'normalize-space((//div[@class="designations"]/h2)['+str(k+1)+'])'
        nom_prod.append(response.xpath(xpath_nom).extract()[0])

    url_prod = response.xpath('//div[@class="designations"]/h2/a/@href').extract()

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'https://www.boulanger.com'
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")

    item = response.meta['item']
    nom_prod = response.meta['nom_prod']
    counter = response.meta['counter']

    #Detalles
    detail_count = int(float(response.xpath('count(//li[@class="bestpoint"])').extract()[0]))
    detail_prod = []
    for k in range(detail_count):
        detail_xpath = '//li[@class="bestpoint"][' +str(k+1)+ ']'
        detail_prod.append(response.xpath('normalize-space('+detail_xpath+')').extract()[0])



    url_tienda = 'https://www.boulanger.com' + response.meta['url_tienda']

    #Ficha Tecnica
    ficha_izq = cleanhtml(response.xpath('//table[@class="characteristic"]/tbody/tr/td/span/text()[1][normalize-space()]').extract())
    ficha_der = cleanhtml(response.xpath('//table[@class="characteristic"]/tbody/tr/td/text()').extract())
    ficha_izq = [x.replace(":", "") for x in ficha_izq]
    ficha_izq = [" ".join(x.split()) for x in ficha_izq]
    ficha_der = [" ".join(x.split()) for x in ficha_der]

    print("FICHAS BOULANGER")
    print(ficha_izq)
    print(ficha_der)
    ficha_tec={}
    for k in range(len(ficha_izq)):
        # print(ficha_izq[k])
        try:
            if ficha_izq[k][-4:]=='Aide':
                ficha_izq[k]=ficha_izq[k][:-4]
                ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r', '').replace('\t', '').replace('\n', '')
            else:
                ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','')
        except:
            print(ficha_tec)
            print(ficha_izq)
            print(ficha_der)
            ficha_tec[ficha_izq[k]] = ficha_der[k].replace('\r','').replace('\t','').replace('\n','')

    #Tienda

    precio = response.xpath('normalize-space(//span[contains(@class,"StrikeoutPrice")])').extract()[0].split(' ')[0].replace('\xa0','').replace(' ','').replace("\u20ac", ".")

    if precio:

        tienda = [{
            'precio': precio + ' EUR',
            'nombre_tienda':'Boulanger',
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

