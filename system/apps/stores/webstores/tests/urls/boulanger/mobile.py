# -*- coding: utf-8 -*-
def urlgen_mobile(filtros):

    fields = {
        'url_base': '',
        'brand': '',
        'systeme_d_exploitation': '',
        'memoire_interne': '',
        'taille_de_l_ecran': '',
        'memoire_ram': '',
        'coloris': ''
    }

    num_filters = 0

    if filtros['Memoire'].replace(" ", "") == "null":
        filtros['Memoire'] = ""

    if filtros['Taille'].replace(" ", "") == "null":
        filtros['Taille'] = ""

    if filtros['Ram'].replace(" ", "") == "null":
        filtros['Ram'] = ""

    fields['url_base'] = "https://www.boulanger.com/c/smartphone-telephone-portable"

    # Marque
    if filtros["Marque"]:
        num_filters += 1
        fields['brand'] = 'brand~' + filtros['Marque'].lower().replace(" ", "20")


    # OS
    if filtros["Systeme dexploitation"] and not filtros["Marque"]:
        num_filters += 1
        if filtros['Systeme dexploitation'] == 'Android':
            fields['systeme_d_exploitation'] = 'facettes_gsm_____systeme_d_exploitation~android'
        elif filtros['Systeme dexploitation'] == 'Apple iOS':
            fields['systeme_d_exploitation'] = 'facettes_gsm_____systeme_d_exploitation~ios'


    # Memoria
    if filtros['Memoire']:
        num_filters += 1
        if float(filtros['Memoire']) >= 64:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~6420go;12820go;25620go'
        elif float(filtros['Memoire']) >= 32:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~25620go;12820go;6420go;3220go'
        elif float(filtros['Memoire']) >= 16:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~12820go;6420go;3220mo;1620go'
        elif float(filtros['Memoire']) >= 8:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~6420go;3220mo;1620go;820go'
        elif float(filtros['Memoire']) >= 4:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~3220mo;1620go;820go;420mo'
        elif float(filtros['Memoire']) >= 4:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~1620go;820go;420mo;120go'


    if filtros['Taille']:
        num_filters += 1
        if float(filtros['Taille']) < 5.0:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~22c42220soit2062c120cm;42c72220soit20112c920cm;22c32220soit2052c820cm;12c772220soit2042c4920cm;42220soit20102c120cm;42c52220soit20112c420cm;42c82220soit20122c220cm;12c72220soit2042c320cm;12c82220soit2042c620cm;42c62220soit20112c720cm;22c82220soit2072c120cm;32c52220soit2082c920cm;22c22220soit2052c620cm;22220soit20520cm;22c62220soit2062c620cm'
        elif float(filtros['Taille']) >= 5.0 and float(filtros['Taille']) <= 5.5:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~52c52220soit201420cm;52c22220soit20132c220cm;52c12220soit20122c920cm;52220soit20122c720cm;52c32220soit20132c520cm'
        if float(filtros['Taille']) > 5.5:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~52c62220soit20142c220cm|facettes_gsm_____taille_de_l_ecran~52c72220soit20142c520cm;62c22220soit20152c720cm;52c82220soit20142c520cm;62220soit20152c2420cm;52c72220soit20142e2620cm;62c32220soit201620cm;62c42220soit20162c2520cm;52c92220soit20142c520cm'


    if filtros['Ram']:
        num_filters += 1
        if int(filtros['Ram']) >= 4:
            fields['memoire_ram'] = 'memoire_____memoire_ram~820go;620go;420go'
        if int(filtros['Ram']) >= 2:
            fields['memoire_ram'] = 'memoire_____memoire_ram~220go;320go;420go'
        elif int(filtros['Ram']) < 2:
            fields['memoire_ram'] = 'memoire_____memoire_ram~3220mo;6420mo;12c520go;120go;420mo;1620mo;820mo;51220mo;02c2520go'

    # COULEURS
    # if filtros['Couleur']:
    #     num_filters += 1
    #     if filtros['Couleur'] == 'Noir':
    #         fields['coloris'] = 'facettes_communes_____coloris~noir'
    #     elif filtros['Couleur'] == 'Violet':
    #         fields['coloris'] = 'facettes_communes_____coloris~violet'
    #     elif filtros['Couleur'] == 'Beige':
    #         fields['coloris'] = 'facettes_communes_____coloris~beige'
    #     elif filtros['Couleur'] == 'Blanc':
    #         fields['coloris'] = 'facettes_communes_____coloris~blanc'
    #     elif filtros['Couleur'] == 'Bleu':
    #         fields['coloris'] = 'facettes_communes_____coloris~bleu'
    #     elif filtros['Couleur'] == 'Or':
    #         fields['coloris'] = 'facettes_communes_____coloris~dore'
    #     elif filtros['Couleur'] in ['Gris', 'Argent']:
    #         fields['coloris'] = 'facettes_communes_____coloris~gris'
    #     elif filtros['Couleur'] == 'Jaune':
    #         fields['coloris'] = 'facettes_communes_____coloris~dore'
    #     elif filtros['Couleur'] == 'Orange':
    #         fields['coloris'] = 'facettes_communes_____coloris~orange'
    #     elif filtros['Couleur'] == 'Rose':
    #         fields['coloris'] = 'facettes_communes_____coloris~rose'
    #     elif filtros['Couleur'] == 'Rouge':
    #         fields['coloris'] = 'facettes_communes_____coloris~rouge'
    #     elif filtros['Couleur'] == 'Vert':
    #         fields['coloris'] = 'facettes_communes_____coloris~vert'


    url = fields['url_base']
    sorting = 'sorting_price=asc'
    url_fields = []

    if num_filters > 1:
        url = 'https://www.boulanger.com/c/nav-filtre/smartphone-telephone-portable'
        sorting = '&' + sorting

    if num_filters == 1:
        url += '/'
        sorting = '?' + sorting
    else:
        url += '?'

    if fields['brand']:
        url_fields.append(fields['brand'])
    if fields['systeme_d_exploitation']:
        url_fields.append(fields['systeme_d_exploitation'])
    if fields['memoire_interne']:
        url_fields.append(fields['memoire_interne'])
    if fields['taille_de_l_ecran']:
        url_fields.append(fields['taille_de_l_ecran'])
    if fields['memoire_ram']:
        url_fields.append(fields['memoire_ram'])
    if fields['coloris']:
        url_fields.append(fields['coloris'])

    url += "|".join(url_fields)
    url += sorting

    return url


filtros = {
    'Marque': 'SAMSUNG',
    'Memoire': '12',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Taille': '5.0',
    'Ram': '6',
    'Systeme dexploitation': 'Android'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': 'SAMSUNG',
    'Memoire': '8',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Taille': '7',
    'Ram': '3',
    'Systeme dexploitation': 'Android'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Memoire': '8',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Taille': '7',
    'Ram': '3',
    'Systeme dexploitation': 'Android'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Memoire': '',
    'Couleur': '',
    'Resolution': '',
    'Taille': '',
    'Ram': '',
    'Systeme dexploitation': ''
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': 'APPLE',
    'Memoire': '8',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Taille': '7',
    'Ram': '3',
    'Systeme dexploitation': 'Apple iOS'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Memoire': '',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Taille': '5',
    'Ram': '3',
    'Systeme dexploitation': 'Apple iOS'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")
