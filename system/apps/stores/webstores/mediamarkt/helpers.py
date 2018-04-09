def urlgen_tv(filtros, should_print):
    
    url_mediamarkt = 'https://tiendas.mediamarkt.es/televisores'

    # Preprocesamiento
    if filtros['TaillePounce'] and filtros['TaillePounce'].replace(" ", "") != "null":
        if str(filtros['TaillePounce']).isdigit():

            taille_pounces = int(filtros['TaillePounce'])

            if taille_pounces > 0:
                exist_filter = True

            # TAILLE
            if taille_pounces >= 28 and taille_pounces <= 32:
                url_mediamarkt += '/sc/televisores-28-32-pulgadas.televisores-40-43-pulgadas.televisores-48-50-pulgadas.televisores-55-60-pulgadas.televisores-mas-65-pulgadas'
            elif taille_pounces >= 40 and taille_pounces <= 43:
                url_mediamarkt += '/sc/televisores-40-43-pulgadas.televisores-48-50-pulgadas.televisores-55-60-pulgadas.televisores-mas-65-pulgadas'
            elif taille_pounces >= 48 and taille_pounces <= 50:
                url_mediamarkt += '/sc/televisores-48-50-pulgadas.televisores-55-60-pulgadas.televisores-mas-65-pulgadas'
            elif taille_pounces >= 55 and taille_pounces <= 60:
                url_mediamarkt += '/sc/televisores-55-60-pulgadas.televisores-mas-65-pulgadas'
            elif taille_pounces > 65:
                url_mediamarkt += '/sc/televisores-mas-65-pulgadas'

    # MARQUE
    if filtros['Marque'] != '':
        
        url_mediamarkt += '/m/' + filtros['Marque'].lower().replace(' ', '-')
        if filtros['Marque'].upper() in {"THOMSON","PHILIPS","SHARP","PANASONIC","OK"}:
            url_mediamarkt += '-marca'


    # ORDEN DE PRODUCTOS, ignorado porque lleva productos no interesantes
    # url_mediamarkt += '?orderBy=price&orderByDirection=ASC'

    return url_mediamarkt


def urlgen_mobile(filtros, should_print):
    pass


# -------- FILTROS POSTERIORES
def filter_tv(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products


def filter_mobile(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products
