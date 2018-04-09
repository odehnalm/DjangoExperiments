import json
import re

from lxml import html
import requests
from scrapy import Request as ScrapyRequest

from apps.scrapy_app.scrapy_app.items import ScrapyAppItem
from ...utils import cleanhtml


def init_requests(**kwargs):

    url_pr = kwargs.get("url")
    callback = kwargs.get("callback")

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
        'X-Requested-With': 'XMLHttpRequest'
    }

    yield ScrapyRequest(
        url,
        meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [302]
        },
        headers=headers,
        callback=callback,
        dont_filter=True)


def get_data(response, **kwargs):

    jsonresponse = json.loads(response.body_as_unicode())
    html_response = html.fromstring(jsonresponse['list'])

    nom_prod = html_response.xpath(
        '//div[@class="productname"]//a/text()')
    url_prod = html_response.xpath(
        '//p[@class="productdescription"]/a/@href')
    detail_prod = []

    return {
        'nom_prod': nom_prod,
        'detail_prod': detail_prod,
        'url_prod': url_prod,
        'url_base': 'http://www.pricerunner.fr'
    }


def get_item_data(response):

    print(" -------------------------------------------  GET ITEM DATA METHOD")

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

    return ScrapyRequest(
        url_ofertas,
        callback=parse_ofertas,
        meta={'dont_redirect': True,
              'handle_httpstatus_list': [302],'item': item,'nombre':nombre,'detalles':detail_prod,'ficha_tec':fiche_tec},
        dont_filter=True
    )

def parse_ofertas(response):

    item = response.meta['item']

    nom_tiendas = response.xpath('//h4/a/@retailer-data').extract()

    tiendas = []
    for k in range(len(nom_tiendas)):

        precio = response.xpath('normalize-space((//div[@class="price-content"])[{0}])'.format(k+1)).extract()[0].split(' excl. ')[0].replace("\u20ac", "").replace(',','.').replace(' ','')

        if precio:

            tiendas.append({
                'precio' : precio + ' EUR',
                'nombre_tienda' : nom_tiendas[k].split('(')[0].replace('\xa0',''),
                'url_tienda' : 'http://www.pricerunner.fr' + response.xpath('(//h4/a/@href)[{0}]'.format(k+1)).extract()[0]
            })

    if tiendas:

        item['nombre'] = response.meta['nombre']
        item['detalles'] = response.meta['detalles']
        item['ficha_tecnica'] = response.meta['ficha_tec']
        item['tiendas'] = tiendas

    else:

        item['nombre'] = ""
        item['detalles'] = ""
        item['ficha_tecnica'] = ""
        item['tiendas'] = ""

    yield item

