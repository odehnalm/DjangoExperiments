def urlgen_tv(filtros):

    exist_filter = False
    fields = {
        'x-100311823': '',
        'compatibilite-hd': '',
        'format-d-ecran': '',
        'marque': '',
        'taille-de-la-diagonale': '',
        'type-de-tv': '',
    }

    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-100311823'] = 'c-100311823-televiseur'

    # ---- MARQUE
    if filtros['Marque'] != '':
        exist_filter = True

        if filtros['Marque'].lower() == "lg" or\
                filtros['Marque'].lower() == "philips" or\
                filtros['Marque'].lower() == "samsung" or\
                filtros['Marque'].lower() == "sony" or\
                filtros['Marque'].lower() == "panasonic" or\
                filtros['Marque'].lower() == "toshiba":

            fields['x-100311823'] = 'v-100311823-tv-' + filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')
        else:

            fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # ---- TYPE DE TV
    # if filtros['3D'] and filtros['3D'] == 'Oui':
    #     exist_filter = True
    #     fields['type-de-tv'] = 'tv-3d'

    # if fields['type-de-tv'] == '' and filtros['Type'] != '':
    if filtros['Type'] != '':
        exist_filter = True

        if filtros['Type'] == 'LED':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-led'

            elif 'v-100311823-tv-' in fields['x-100311823']:

                if 'samsung' in fields['x-100311823'] or\
                        'sony' in fields['x-100311823']:
                    fields['x-100311823'] = fields['x-100311823'].replace("v-100311823-tv-", 'v-100311823-tv-led-')

                else:
                    fields['type-de-tv'] = "tv-led"

        elif filtros['Type'] == 'LCD':

            fields['type-de-tv'] = 'tv-lcd'

        elif filtros['Type'] == 'OLED':

            fields['type-de-tv'] = 'oled'

    # ---- COMPATIBILITE HD
    if filtros['Resolution'] and '' not in filtros['Resolution']:
        exist_filter = True

        if filtros['Resolution'][0] == '1080p':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-full-hd'

            elif fields['x-100311823'] == 'v-100311823-tv-led':

                fields['x-100311823'] = 'v-100311823-tv-full-hd'
                fields['type-de-tv'] = "tv-led"

            else:

                fields['compatibilite-hd'] = "full-hd"

        elif filtros['Resolution'][0] == '720p':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-hd-ready'

            elif fields['x-100311823'] == 'v-100311823-tv-led':

                fields['x-100311823'] = 'v-100311823-tv-hd-ready'
                fields['type-de-tv'] = "tv-led"

            else:

                fields['compatibilite-hd'] = "hd-ready"

        elif filtros['Resolution'][0] == '4k':

            fields['compatibilite-hd'] = "ultra-hd-4k"

    # ---- RATIO
    if filtros['Ratio'] and '' not in filtros['Ratio']:
        exist_filter = True
        if filtros['Ratio'][0] == '4:3':
            fields['format-d-ecran'] = '4-3'
        elif filtros['Ratio'][0] == '16:9':
            fields['format-d-ecran'] = '16-9'

    # ---- PULGADAS
    if filtros['TaillePounce'] and\
            filtros['TaillePounce'].replace(" ", "") != "null":
        if str(filtros['TaillePounce']).isdigit():

            taille_pounces = int(filtros['TaillePounce'])

            if taille_pounces > 0:
                exist_filter = True

            # TAILLE
            if taille_pounces > 0 and taille_pounces < 24:
                fields['taille-de-la-diagonale'] = 'moins-de-24-61cm'
            elif taille_pounces >= 24 and taille_pounces <= 32:
                fields['taille-de-la-diagonale'] = '24-61cm-a-32-82cm'
            elif taille_pounces >= 37 and taille_pounces <= 42:
                fields['taille-de-la-diagonale'] = '37-94cm-a-42-107cm'
            elif taille_pounces >= 46 and taille_pounces <= 50:
                fields['taille-de-la-diagonale'] = '46-116cm-a-50-127cm'
            elif taille_pounces >= 55 and taille_pounces <= 60:
                fields['taille-de-la-diagonale'] = '55-140cm-a-60-152cm'
            elif taille_pounces > 60:
                fields['taille-de-la-diagonale'] = 'plus-de-60-152cm'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100311823']
    if fields['compatibilite-hd']:
        counter_fields += 1
        url_kelkoo += '/compatibilite-hd/' + fields['compatibilite-hd']
    if fields['format-d-ecran']:
        counter_fields += 1
        url_kelkoo += '/format-d-ecran/' + fields['format-d-ecran']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['taille-de-la-diagonale']:
        counter_fields += 1
        url_kelkoo += '/taille-de-la-diagonale/' + fields['taille-de-la-diagonale']
    if fields['type-de-tv']:
        counter_fields += 1
        url_kelkoo += '/type-de-tv/' + fields['type-de-tv']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo


filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '70',
    "Type": 'LED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': 'LG',
    "TaillePounce": '70',
    "Type": 'LED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '40',
    "Type": 'LED',
    "Resolution": ['1080p'],
    "Ratio": ['16:9'],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': 'TOSHIBA',
    "TaillePounce": '40',
    "Type": 'LED',
    "Resolution": ['1080p'],
    "Ratio": ['16:9'],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': 'AKIA',
    "TaillePounce": '40',
    "Type": 'LED',
    "Resolution": ['720p'],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '40',
    "Type": 'LED',
    "Resolution": [''],
    "Ratio": ['4:3'],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': 'THOMPSON',
    "TaillePounce": '40',
    "Type": 'LED',
    "Resolution": [''],
    "Ratio": ['4:3'],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": 'LED',
    "Resolution": [''],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": 'OLED',
    "Resolution": [''],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "Oui"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": '',
    "Resolution": ['720p'],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")
