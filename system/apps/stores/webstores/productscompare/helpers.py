def urlgen_tv(filtros, should_print):
    
    fields = {
        'type': '',
        'marque': '',
        'taille': '',
        'resolution': '',
        'design' : ''
    }

    url_lcdcmp = 'http://www.lcd-compare.com/tv-liste-122.htm?'

    # Marque
    if filtros['Marque']:
        url_lcdcmp += '&brand=' + filtros['Marque'].upper()

    # Range de prix
    # url_lcdcmp += "".join(('&price=',filtros['Range_prix'][0],'-',filtros['Range_prix'][1]))

    # Resolution
    resoluciones_lcdcmp = ''
    if filtros['Resolution'][0]:
        if '4K' in filtros['Resolution']:
            resoluciones_lcdcmp += '7,8'
        elif '1080p' in filtros['Resolution']:
            resoluciones_lcdcmp += '6,7,8'
        elif '720p' in filtros['Resolution']:
            resoluciones_lcdcmp += '2,6,7,8'
        if resoluciones_lcdcmp[-1] == ',': resoluciones_lcdcmp[-1] = []
        url_lcdcmp += '&tv_label=' + resoluciones_lcdcmp

    # Type: categoria exclusiva, al no incluirla tenemos ambos productos LED y OLED
    if filtros['Type'] == 'OLED': url_lcdcmp += '&blk_type=4'

    # Taille: rango de pulgadas, si no hay rango, se considera hasta el mayor tamano(300cm)
    if filtros['TailleCm'] != '0':
        url_lcdcmp += '&visiplancm=' + filtros['TailleCm'] + '-' + str(300)

    # Refresh
    if filtros['Refresh'] == '200':
        url_lcdcmp += '&motion=200'
    elif filtros['Refresh'] == '100':
        url_lcdcmp += '&motion=100,200'
    elif filtros['Refresh'] == '50':
        url_lcdcmp += '&motion=50,100,200'

    # Indice_de_fluidite
    if filtros['Indice_refresh']:
        url_lcdcmp += '&indmotionlcd=' + filtros['Indice_refresh'] + '-4000'

    # 3D
    if filtros['3D'] == 'Oui': url_lcdcmp += '&3d=1'

    # HDR
    if len(filtros['HDR']) > 0:
        url_lcdcmp += '&hdr=1'
        if 'Dolby Vision' in filtros['HDR']: url_lcdcmp += '&hdrdb=1'
        if 'HLG' in filtros['HDR']: url_lcdcmp += '&hdrhlg=1'
        if 'HDR10' in filtros['HDR']: url_lcdcmp += '&hdr10=1'

    # SMART: internet
    if filtros['Smart'] == 'Oui':
        if filtros['Internet'] == 'Oui':
            url_lcdcmp += '&internet=1'

    # Wifi
    if filtros['Wifi'] == 'Oui':
        url_lcdcmp += '&wifi=1'

    # Couleur ()
    if type(filtros['Couleur']) == str and filtros['Couleur']:
        if filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent': url_lcdcmp += '&color=CECECE'
        if filtros['Couleur'] == 'Noir': url_lcdcmp += '&color=000000'
        if filtros['Couleur'] == 'Blanc': url_lcdcmp += '&color=FFFFFF'

    # Design
    if 'Incurve' in filtros['Design']: url_lcdcmp += '&screen_curved=1'

    # Energy
    if filtros['Energy']:
        url_lcdcmp += '&energyclass='
        if filtros['Energy'] == 'A++': url_lcdcmp += 'a2p'
        if filtros['Energy'] == 'A+': url_lcdcmp += 'a2p,a1p'
        if filtros['Energy'] == 'A': url_lcdcmp += 'a2p,a1p,a'
        if filtros['Energy'] == 'B' or filtros['Energy'] == 'C': url_lcdcmp += 'a2p,a1p,a,b'


    return url_lcdcmp


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
