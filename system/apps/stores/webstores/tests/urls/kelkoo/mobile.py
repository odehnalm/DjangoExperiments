def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def urlgen_mobile(filtros):

    exist_filter = False
    fields = {
        'x-100020213': '',
        'marque': '',
        'systeme-d-exploitation': '',
        'resolution-de-l-appareil-photo': ''
    }

    url_kelkoo = 'http://www.kelkoo.fr/'
    fields['x-100020213'] = 'c-100020213-telephone-portable-sans-abonnement'

    if filtros['MegapixelsArriere'] == "null":
        filtros['MegapixelsArriere'] = ""

    # ---- MARQUE
    if filtros['Marque']:
        exist_filter = True

        if filtros['Marque'].lower() == "htc" or\
                filtros['Marque'].lower() == "nokia" or\
                filtros['Marque'].lower() == "samsung":

            fields['x-100020213'] = 'v-100020213-telephone-portable-' + filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

        elif filtros['Marque'].lower() == "apple":
            fields['x-100020213'] = 'v-100020213-iphone'

        elif filtros['Marque'].lower() == "blackberry":
            fields['x-100020213'] = 'v-100020213-blackberry'

        else:
            fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # ---- SYSTEME D EXPLOITATION
    if filtros['Systeme dexploitation']:
        exist_filter = True

        if filtros['Systeme dexploitation'] == 'Android':
            fields['systeme-d-exploitation'] = 'android'
        elif filtros['Systeme dexploitation'] == 'Apple iOS':
            fields['systeme-d-exploitation'] = 'apple-ios'
        elif filtros['Systeme dexploitation'] == 'BlackBerry':
            fields['systeme-d-exploitation'] = 'blackberry-os'
        elif filtros['Systeme dexploitation'] == 'Windows Phone':
            fields['systeme-d-exploitation'] = 'windows-phone'
        elif filtros['Systeme dexploitation'] == 'Windows Phone':
            fields['systeme-d-exploitation'] = 'windows-phone'

    # ---- RESOLUTION DE L APPAREIL PHOTO
    if filtros['MegapixelsArriere'] and isfloat(filtros['MegapixelsArriere']):

        mega_pixels = float(filtros['MegapixelsArriere'])
        exist_filter = True  

        if mega_pixels<1:
            fields['resolution-de-l-appareil-photo'] = 'moins-de-1-megapixel'
        elif mega_pixels>=1 and mega_pixels<=2:
            fields['resolution-de-l-appareil-photo'] = 'entre-1-et-2-megapixels'
        elif mega_pixels>2 and mega_pixels<=3:
            fields['resolution-de-l-appareil-photo'] = 'entre-2-1-et-3-megapixels'
        elif mega_pixels>3 and mega_pixels<=4:
            fields['resolution-de-l-appareil-photo'] = 'entre-3-1-et-4-megapixels'
        elif mega_pixels>4 and mega_pixels<=5:
            fields['resolution-de-l-appareil-photo'] = 'entre-4-1-et-5-megapixels'
        elif mega_pixels>5:
            fields['resolution-de-l-appareil-photo'] = 'plus-de-5-megapixels'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100020213']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['resolution-de-l-appareil-photo']:
        counter_fields += 1
        url_kelkoo += '/resolution-de-l-appareil-photo/' + fields['resolution-de-l-appareil-photo']
    if fields['systeme-d-exploitation']:
        counter_fields += 1
        url_kelkoo += '/systeme-d-exploitation/' + fields['systeme-d-exploitation']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo


filtros = {
    'Marque': 'Apple',
    'Systeme dexploitation': 'Apple iOS',
    'MegapixelsArriere': "4.5",
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/v-100020213-iphone/resolution-de-l-appareil-photo/entre-4-1-et-5-megapixels/systeme-d-exploitation/apple-ios?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': 'Sony',
    'Systeme dexploitation': 'Android',
    'MegapixelsArriere': "5",
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/nf/c-100020213-telephone-portable-sans-abonnement/marque/sony/resolution-de-l-appareil-photo/entre-4-1-et-5-megapixels/systeme-d-exploitation/android?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Systeme dexploitation': '',
    'MegapixelsArriere': "null",
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/c-100020213-telephone-portable-sans-abonnement.html?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Systeme dexploitation': 'Windows Phone',
    'MegapixelsArriere': "null",
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/c-100020213-telephone-portable-sans-abonnement/systeme-d-exploitation/windows-phone?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")
